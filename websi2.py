import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import requests

def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(
        r"C:\Users\anubh\OneDrive\Desktop\my-project-1-447821-2cddca709421.json",
        scopes=scope
    )
    client = gspread.authorize(creds)
    
    # Open the specific Google Sheet by ID
    sheet = client.open_by_key("15qy-ai-zCHdX02-oX3KwJIzfRNaPJDZSjz1-XiYPKp4").sheet1
    return sheet

def send_email_via_brevo(to_email):
    api_url = "https://api.brevo.com/v3/smtp/email"
    api_key = "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"  # Replace with your Brevo API Key
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }
    data = {
        "sender": {"name": "180 Degrees Consulting", "email": "anubhootijain007@gmail.com"},
        "to": [{"email": to_email}],
        "subject": "Thank You for Your Feedback",
        "htmlContent": """
        <p>Hello,</p>
        <p>Thank you for your valuable feedback. We have received your complaint and will review it shortly.</p>
        <p>Best Regards,<br>180 Degrees Consulting</p>
        """
    }
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Thank you email sent to {to_email}")
    else:
        print(f"Failed to send email to {to_email}: {response.text}")

def submit_feedback(company, client_name, client_email, complaint_type, issue_desc, stop_emails):
    sheet = connect_to_gsheet()
    sheet.append_row([company, client_name, client_email, ", ".join(complaint_type), issue_desc, stop_emails])
    send_email_via_brevo(client_email)
    st.success("Thank you! Your feedback has been recorded.")

# Streamlit UI
# Set background color to light green
page_bg = """
<style>
body {
    background-color: #dfffdf;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("Client Feedback Portal")

company_name = st.text_input("Company Name", "")
client_name = st.text_input("Client Name", "")
client_email = st.text_input("Client Email", "")

complaint_options = [
    "Communication", "Responsiveness", "Project Execution", "Documentation",
    "Clarity", "Professionalism", "Engagement", "Data Representation Accuracy",
    "Business Understanding", "Reporting Transparency", "Overall Satisfaction", "Others"
]
complaint_type = st.multiselect("What aspect would you like to give feedback on?", complaint_options)

issue_desc = st.text_area("Describe your issue here")
stop_emails = st.checkbox("I don't want to receive such emails anymore")

if st.button("Submit Feedback"):
    if company_name and client_name and client_email and issue_desc:
        submit_feedback(company_name, client_name, client_email, complaint_type, issue_desc, "Yes" if stop_emails else "No")
    else:
        st.warning("Please fill in all fields before submitting.")
