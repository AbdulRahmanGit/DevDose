import traceback
import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from database import get_db, add_user, delete_user, update_user, fetch_details,User  # Ensure User model is imported
from email_utils import send_email
from otp import *
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "https://devdose.vercel.app", 
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow all origins (consider restricting in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    language: str
    difficulty: str

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerification(BaseModel):
    email: EmailStr
    otp: str

class UserUpdate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    language: Optional[str] = None
    difficulty: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to Devdose"}
@app.get("/register")
def read_root():
    return {"message": "Welcome to Devdose"}
@app.post("/register")
def register_user(user: UserRegistration, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered with this email.")
    
    try:
        add_user(db, user.name, user.email, user.language, user.difficulty)
        send_email(
            subject=f"Welcome to Devdose, {user.name}!",
            body=f"Thank you for registering. You'll start receiving {user.language} tips of {user.difficulty} level soon!",
            recipient=user.email
        )
        return {"message": "User registered successfully, check your mail"}
    except HTTPException as http_exc:
        # Log HTTPException separately if needed
        logging.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        logging.error(f"Unexpected error in request_update_otp: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/request-delete-otp")
async def request_delete_otp(request: Request, db: Session = Depends(get_db)):
    try:
        request_data = await request.json()
        email_str = request_data.get("email")
        
        if not email_str:
            raise HTTPException(status_code=400, detail="Email is required")

        existing_user = db.query(User).filter(User.email == email_str).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        otp = generate_otp()
        store_otp(email_str, otp)  # Ensure this works as expected

        print(f"OTP Store after storing: {otp_store}")  # Debugging print

        send_email(
            subject="Your OTP for Account Deletion",
            body=f"Hello,\n\nYour OTP for account deletion is: {otp}.\n\nPlease use this OTP to confirm account deletion.",
            recipient=email_str
        )
        return {"message": "An OTP has been sent to your email. Please use it to confirm deletion."}
    except HTTPException as http_exc:
        # Log HTTPException separately if needed
        logging.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        logging.error(f"Unexpected error in request_update_otp: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
@app.post("/delete")
async def delete_user_account(request: Request, db: Session = Depends(get_db)):
    try:
        request_data = await request.json()
        print(request_data)
        email_str = request_data.get("email")
        otp = request_data.get("otp")
        
        if not email_str:
            raise HTTPException(status_code=400, detail="Email is required")
        if not otp:
            raise HTTPException(status_code=400, detail="OTP is required")

        # Verify OTP
        stored_otp = otp_store.get(email_str)
        print(f"Stored OTP for {email_str}: {stored_otp}")
        print(f"Received OTP: {otp}")
        
        if not stored_otp or str(otp) != stored_otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # Delete the user
        existing_user = db.query(User).filter(User.email == email_str).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        delete_user(db, email_str)
        otp_store.pop(email_str, None)  # Remove OTP after successful deletion
        return {"message": f"User with email {email_str} has been successfully deleted."}
    except HTTPException as http_exc:
        # Log HTTPException separately if needed
        logging.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        logging.error(f"Unexpected error in request_update_otp: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/request-update-otp")
async def request_update_otp(request: Request, db: Session = Depends(get_db)):
    try:
        request_data = await request.json()
        email_str = request_data.get("email")
        
        if not email_str:
            raise HTTPException(status_code=400, detail="Email is required")

        existing_user = db.query(User).filter(User.email == email_str).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        otp = generate_otp()
        store_otp(email_str, otp)  # Use the store_otp function

        print(f"OTP Store: {otp_store}")  # Debugging print

        send_email(
            subject="Your OTP for Updating User Details",
            body=f"Hello,\n\nYour OTP for updating user details is: {otp}.\n\nPlease use this OTP to confirm the update.",
            recipient=email_str
        )
        return {"message": "An OTP has been sent to your email. Please use it to confirm the update."}
    except HTTPException as http_exc:
        # Log HTTPException separately if needed
        logging.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        logging.error(f"Unexpected error in request_update_otp: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
@app.post("/update")
async def update_user_account(request: Request, db: Session = Depends(get_db)):
    try:
        request_data = await request.json()
        email_str = request_data.get("email")
        otp = request_data.get("otp")
        name = request_data.get("name")
        language = request_data.get("language")
        difficulty = request_data.get("difficulty")
        
        if not email_str or not otp:
            raise HTTPException(status_code=400, detail="Email and OTP are required")

        # Verify OTP
        stored_otp = otp_store.get(email_str)
        if not stored_otp or str(otp) != stored_otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # Update the user
        existing_user = db.query(User).filter(User.email == email_str).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        update_user(db, email_str, name, language, difficulty)
        otp_store.pop(email_str, None)  # Remove OTP after successful update
        return {"message": f"User with email {email_str} has been successfully updated."}
    except HTTPException as http_exc:
        # Log HTTPException separately if needed
        logging.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        logging.error(f"Unexpected error in request_update_otp: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
class UserDetail(BaseModel):
    name: str
    language: str
    difficulty: str

@app.get("/fetch-details", response_model=UserDetail)
async def fetch_user_details(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return UserDetail(name=user.name, language=user.language, difficulty=user.difficulty)
    else:
        raise HTTPException(status_code=404, detail="User not found")
def main():
    uvicorn.run(app, port=8000, host="0.0.0.0")

if __name__ == "__main__":
    main()
