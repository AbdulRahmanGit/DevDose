from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, get_db, add_user, fetch_users, User
from email_utils import send_email
from generator import generate_tips
from jinja2 import Template
from fastapi.middleware.cors import CORSMiddleware
import schedule
import time
import threading
import uvicorn
app = FastAPI()

# Add CORS middleware
orig_cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=orig_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to DevDoses"}

# Define Pydantic model for the registration request
class UserRegistration(BaseModel):
    name: str
    email: str
    language: str
    difficulty: str

@app.post("/job")
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
@app.post("/schedule")
def schedule_job():
    schedule.every().day.at("09:00").do(job)
    print("scheduled at 9 AM")
    #schedule.every().minute.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduling in a separate thread
def start_scheduler():
    scheduler_thread = threading.Thread(target=schedule_job)
    scheduler_thread.daemon = True
    scheduler_thread.start()
def main():
    job()
if __name__ == "__main__":
    #schedule_job()
    # Start the scheduler thread
    #start_scheduler()
    #temp 
    #job()
    main()
    # Run the FastAPI server
