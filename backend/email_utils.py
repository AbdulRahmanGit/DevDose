import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from database import fetch_users
from generator import generate_tips
from dotenv import load_dotenv
import os
load_dotenv()
def send_email(subject, body, to_email):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
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
        
        with open('templates/email_template.html') as file:
            template = Template(file.read())
        
        html_content = template.render(subject=f"{difficulty.capitalize()} {language} Tips", body=tips, name=name)
        send_email(f"{difficulty.capitalize()} {language} Tips", html_content, email)
