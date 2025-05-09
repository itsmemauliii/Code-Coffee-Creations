import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from notion_client import Client
from datetime import datetime

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("JobTracker").sheet1  # Your Google Sheet name

# Notion setup
notion = Client(auth="your_notion_secret_api_key")  # Replace with your Notion API key
notion_database_id = "your_database_id"  # Replace with your Notion database ID

# Function to append data to Google Sheets
def append_to_google_sheets(job_title, company, platform, status, notes):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([date, job_title, company, platform, status, notes])

# Function to append data to Notion
def append_to_notion(job_title, company, platform, status, notes):
    notion.pages.create(
        parent={"database_id": notion_database_id},
        properties={
            "Job Title": {"title": [{"text": {"content": job_title}}]},
            "Company": {"rich_text": [{"text": {"content": company}}]},
            "Platform": {"select": {"name": platform}},
            "Status": {"select": {"name": status}},
            "Notes": {"rich_text": [{"text": {"content": notes}}]},
            "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}
        }
    )

# Streamlit form to collect job application data
with st.form("job_application_form"):
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    platform = st.selectbox("Platform", ["LinkedIn", "Company Website", "Indeed", "Other"])
    status = st.selectbox("Status", ["Applied", "Interviewing", "Rejected", "Offer"])
    notes = st.text_area("Notes")
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Add job data to Google Sheets
        append_to_google_sheets(job_title, company, platform, status, notes)
        st.success("Job application added to Google Sheets!")

        # Add job data to Notion
        append_to_notion(job_title, company, platform, status, notes)
        st.success("Job application added to Notion!")
