from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, get_db, add_user, fetch_users
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

@app.post("/register")
def register_user(user: UserRegistration, db: Session = Depends(get_db)):
    try:
        add_user(db, user.name, user.email, user.language, user.difficulty)
        send_email(f"Welcome to DevDoses, {user.name}!",
                   "Thank you for registering. You'll start receiving tips soon!",
                   user.email)
        return {"message": "User registered successfully, check your mail"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

# Start the scheduling in a separate thread
def start_scheduler():
    scheduler_thread = threading.Thread(target=schedule_job)
    scheduler_thread.daemon = True
    scheduler_thread.start()

if __name__ == "__main__":
    # Start the scheduler thread
    #start_scheduler()
    #temp 
    job()
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=10000)
