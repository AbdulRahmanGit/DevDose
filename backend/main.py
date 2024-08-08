from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, get_db, add_user, fetch_users
from email_utils import send_email
from generator import generate_tips
from jinja2 import Template
import schedule
import time
import uvicorn


app = FastAPI()

# Define Pydantic model for the registration request
class UserRegistration(BaseModel):
    name: str
    email: str
    language: str
    difficulty: str

@app.post("/api/register")
def register_user(user: UserRegistration, db: Session = Depends(get_db)):
    add_user(db, user.name, user.email, user.language, user.difficulty)
    return {"message": "User registered successfully"}

def job():
    db = SessionLocal()
    try:
        users = fetch_users(db)
        for user in users:
            name, email, language, difficulty = user.name, user.email, user.language, user.difficulty
            tips = generate_tips(name, language, difficulty)
            with open('email_template.html') as file:
                template = Template(file.read())
            html_content = template.render(subject=f"{difficulty.capitalize()} {language} Tips", body=tips, name=name)
            send_email(f"{difficulty.capitalize()} {language} Tips", html_content, email)
    finally:
        db.close()

def schedule_job():
    schedule.every().day.at("09:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Start the FastAPI application or run scheduled job.")
    parser.add_argument('--job', action='store_true', help="Run the scheduled job")
    args = parser.parse_args()

    if args.job:
        schedule_job()
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
