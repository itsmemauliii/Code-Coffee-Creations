# 🧭 Job Application Tracker App

A clean, focused Streamlit app to track your daily job applications, platforms used, follow-up reminders, and more built for those grinding through job portals every single day.

---

## 🚀 Features

✅ Add job applications with:

* Job Title
* Company
* Platform (LinkedIn, Company Website, etc.)
* Status (Applied, Interviewing, Rejected, Offer)
* Notes & custom follow-up details

📊 Visual Dashboard:

* Track total applications
* Track today's applications
* Visual status distribution bar chart
* Live editable data table

📤 Export Functionality:

* Download your application log as CSV anytime

🔔 Follow-Up Reminder System:

* Automatically reminds you to follow up after 7 days
* Never miss a potential callback!

🛑 Duplicate Detection:

* Warns if you've already logged the same job/company combo

📅 Optional Cloud Sync:

* **Google Sheets Integration:** Automatically append every new entry to a shared Google Sheet using `gspread`
* **Notion Sync:** Push each application to a Notion database using the official Notion API

---

## 🌟 What Makes It Unique?

💡 Unlike generic task or note apps, this tracker is built **specifically for job seekers**:

* Tracks **daily applications** to help you stay consistent
* Reminds you when to **follow up automatically**
* Prevents **duplicate logs** so your list stays clean
* Built using **Streamlit** — meaning it’s fully customizable, lightweight, and fast
* **Syncs with your cloud tools** (Notion / Google Sheets)
* Designed for **clarity and focus**, not bloat

Ideal for students, freshers, or professionals applying to 100+ job portals!

---

## 🧑‍💻 How to Run

1. **Install packages:**

   ```bash
   pip install streamlit pandas gspread oauth2client notion-client
   ```

2. **Save the code to a file (e.g., `app.py`).**

3. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

---

## 🧠 Ideas for Expansion

* AI resume and JD matcher
* Login and multi-user support
* Notification reminders via email

---

## 🙌 Made With Purpose

Built to solve the stress of chaotic job applications. A tool made **by a job seeker, for job seekers** — track smarter, not harder.

---

📬 Feedback, forks, and feature requests welcome!
