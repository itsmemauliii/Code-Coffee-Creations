import streamlit as st
import pandas as pd
import datetime
import base64
import os

# Initialize session state
if 'job_data' not in st.session_state:
    st.session_state['job_data'] = pd.DataFrame(columns=[
        'Date', 'Job Title', 'Company', 'Platform', 'Status', 'Notes'
    ])

st.set_page_config(page_title="Job Application Tracker", layout="wide")

st.title("📌 Job Application Tracker")
st.markdown("Keep track of every job you apply to and stay organized during your job hunt!")

# Form to input new job application
with st.form("job_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date of Application", datetime.date.today())
        job_title = st.text_input("Job Title")
        company = st.text_input("Company Name")
    with col2:
        platform = st.selectbox("Platform", ["LinkedIn", "Company Website", "Indeed", "Other"])
        status = st.selectbox("Application Status", ["Applied", "Interviewing", "Rejected", "Offer"])
        notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Application")

    if submitted:
        new_entry = {
            'Date': date,
            'Job Title': job_title,
            'Company': company,
            'Platform': platform,
            'Status': status,
            'Notes': notes
        }
        # Check for duplicates
        is_duplicate = ((st.session_state.job_data['Job Title'] == job_title) &
                        (st.session_state.job_data['Company'] == company)).any()
        if is_duplicate:
            st.warning("You've already added this job application.")
        else:
            st.session_state.job_data = pd.concat([
                st.session_state.job_data,
                pd.DataFrame([new_entry])
            ], ignore_index=True)
            st.success("Application added!")

# Dashboard
st.subheader("📊 Your Application Dashboard")
if not st.session_state.job_data.empty:
    df = st.session_state.job_data
    st.dataframe(df)

    # Summary stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Applications", len(df))
        st.metric("Applications Today", (df['Date'] == datetime.date.today()).sum())
    with col2:
        status_counts = df['Status'].value_counts()
        st.bar_chart(status_counts)

    # Export CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "applications.csv", "text/csv")

    # Follow-up Reminder
    st.subheader("🔔 Follow-up Reminders")
    follow_up_days = 7
    df['Date'] = pd.to_datetime(df['Date'])
    due_follow_up = df[df['Date'] + pd.Timedelta(days=follow_up_days) <= pd.Timestamp.today()]
    if not due_follow_up.empty:
        st.warning("Consider following up with these applications:")
        st.dataframe(due_follow_up[['Date', 'Job Title', 'Company', 'Platform']])
    else:
        st.success("No follow-ups needed today!")
else:
    st.info("No applications tracked yet. Use the form above to start!")
