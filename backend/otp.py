import random
import string

# Global dictionary to store OTPs

otp_store = {}
def generate_otp(length=6):
    """Generate a random OTP."""
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return str(otp)

def store_otp(email: str, otp: str):
    """Store OTP in the global dictionary."""
    otp_store[email] = otp

def get_otp(email: str) -> str:
    """Retrieve OTP from the global dictionary."""
    return otp_store.get(email)

def delete_otp(email: str):
    """Delete OTP from the global dictionary."""
    if email in otp_store:
        del otp_store[email]
