import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import datetime
import uuid
import sys
st.write(sys.executable)


# --------- GOOGLE SHEETS SETUP ---------
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"
SHEET_NAME = "Job Tracker"

def get_google_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1_lqAUNnS_GsXiKmN0fH4G-bOJzkp83HjhwVu5Q46kFY/edit")
    worksheet = sheet.get_worksheet(0)
    return worksheet

def append_to_google_sheet(data):
    try:
        sheet = get_google_sheet()
        sheet.append_row(data)
    except Exception as e:
        st.error(f"⚠️ Google Sheets Error: {e}")

# --------- NOTION SETUP ---------
NOTION_DB_ID = "1ee4d7d0503f8047b956e9aa88c09b99"
NOTION_API_KEY = st.secrets["NOTION_API_KEY"]

def append_to_notion(job_data):
    try:
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        payload = {
            "parent": { "database_id": NOTION_DB_ID },
            "properties": {
                "Job Title": { "title": [{ "text": { "content": job_data["title"] }}]},
                "Company": { "rich_text": [{ "text": { "content": job_data["company"] }}]},
                "Platform": { "rich_text": [{ "text": { "content": job_data["platform"] }}]},
                "Status": { "select": { "name": job_data["status"] }},
                "Notes": { "rich_text": [{ "text": { "content": job_data["notes"] }}]},
                "Date": { "date": { "start": job_data["date"] }}
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return True
        else:
            st.error(f"⚠️ Notion Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"⚠️ Notion API Error: {e}")
        return False

# --------- STREAMLIT UI ---------
st.set_page_config(page_title="Job Tracker", page_icon="📌")
st.title("🧭 Job Application Tracker")

with st.form("job_form"):
    col1, col2 = st.columns(2)
    title = col1.text_input("Job Title")
    company = col2.text_input("Company Name")
    platform = st.selectbox("Platform", ["LinkedIn", "Company Website", "Indeed", "Naukri", "Other"])
    status = st.selectbox("Status", ["Applied", "Interviewing", "Rejected", "Offer"])
    notes = st.text_area("Notes")
    submit = st.form_submit_button("Add Application")

if submit:
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    google_data = [today, title, company, platform, status, notes]

    # Append to Google Sheets
    append_to_google_sheet(google_data)

    # Append to Notion
    notion_data = {
        "title": title,
        "company": company,
        "platform": platform,
        "status": status,
        "notes": notes,
        "date": today
    }
    success = append_to_notion(notion_data)

    if success:
        st.success("✅ Application logged in Notion and Google Sheets!")
    else:
        st.error("⚠️ Failed to log to Notion. Please check your API key and database.")
