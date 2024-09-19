#from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from db import SessionLocal, get_db, fetch_users, User, fetch_details
from email_utils import send_email
from generate import generate_tips
from jinja2 import Template
from fastapi import FastAPI
import time
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Pydantic model for the registration request
class UserRegistration(BaseModel):
    name: str
    email: str
    language: str
    difficulty: str



def job(max_retries=3, retry_delay=5):
    db = SessionLocal()
    try:
        users = fetch_users(db) 
        if not users:
            logger.info("No users found.")
            return

        for user in users:
            retries = 0
            while retries < max_retries:
                try:
                    name, email, language, difficulty = user.name, user.email, user.language, user.difficulty
                    tips = generate_tips(name, language, difficulty)
                    template_path = os.path.join(os.path.dirname(__file__), 'template.html')

                    if os.path.isfile(template_path):
                        with open(template_path) as file:
                            template = Template(file.read())

                        subject = f"Devdose Daily Digest - Level Up Your {difficulty} {language} Skills!"
                        unsubscribe_link = f"https://devdose.vercel.app/templates/delete.html"
                        update_link = f"https://devdose.vercel.app/templates/update.html"

                        context = {
                            "header_title": tips.get("header_title", ""),
                            "introduction_greeting": tips.get("introduction_greeting", ""),
                            "introduction_message": tips.get("introduction_message", ""),
                            "programming_tip_title": tips.get("programming_tip_title", ""),
                            "programming_tip_description": tips.get("programming_tip_description", ""),
                            "programming_tip_code": tips.get("programming_tip_code", ""),
                            "programming_tip_output": tips.get("programming_tip_output", ""),
                            "dsa_challenge_title": tips.get("dsa_challenge_title", ""),
                            "dsa_challenge_problem": tips.get("dsa_challenge_problem", ""),
                            "dsa_challenge_solution_steps": tips.get("dsa_challenge_solution_steps", []),
                            "dsa_challenge_code": tips.get("dsa_challenge_code", ""),
                            "dsa_problem_links": tips.get("dsa_problem_links", ""),
                            "footer_message": tips.get("footer_message", ""),
                        }

                        html_content = template.render(context, unsubscribe_link=unsubscribe_link, update_link=update_link)
                        send_email(subject, html_content, email)
                        logger.info(f"Email sent to {email} successfully.")
                        time.sleep(1)
                        break  # Break the retry loop if successful

                    else:
                        logger.error(f"Template file not found at: {template_path}")
                        break  # No need to retry if the template is missing
                except Exception as e:
                    retries += 1
                    logger.error(f"Error processing user {user.name} on attempt {retries}: {e}")
                    if retries < max_retries:
                        logger.info(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        logger.error(f"Max retries reached for user {user.name}. Moving to the next user.")
                
    except Exception as e:
        logger.error(f"Error in job execution: {e}")
    finally:
        db.close()

def main():
    job()

if __name__ == "__main__":
    main()
