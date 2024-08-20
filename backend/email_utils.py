import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from database import fetch_users
from otp import generate_otp
from generate import generate_tips
from dotenv import load_dotenv
import re
import os
load_dotenv()
def send_email(subject, body, recipient):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, recipient, text)
        server.quit()
        print(f"Email sent to {recipient} successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
def send_otp(subject, body, recipient):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, recipient, text)
        server.quit()
        print(f"Email sent to {recipient} successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


def job():
    for user in users:
        users = fetch_users()
    if not users:
        print("No users found. Please register first.")
        return

    for user in users:
        name, email, language, difficulty = user
        tips = generate_tips(name, language, difficulty)
        
        with open('email_template.html') as file:
            template = Template(file.read())
        
          # Render the template
        rendered_content = template.render(body=tips, name=name)
        
        # Extract the subject using regex
        subject_match = re.search(r'^## Subject:\s*(.*)$', rendered_content, re.MULTILINE)
        if subject_match:
            subject = subject_match.group(1)
            # Remove the subject line from the content
            cleaned_html_content = re.sub(r'^## Subject:\s*.*$', '', rendered_content, 1, re.MULTILINE).strip()
        else:
            print(f"Error processing user {name}: Subject not found in the content.")
            continue
        
        # Send the email
        send_email(subject, cleaned_html_content, email)
