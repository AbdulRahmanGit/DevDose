from sqlalchemy import create_engine, Column, String, Integer, inspect
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os
from dotenv import load_dotenv
from typing import Generator

# Load environment variables
load_dotenv()

# Load database connection details from environment variables
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")

# Define the database URL (Either from environment variable or construct manually)
DATABASE_URL = os.getenv("POSTGRES_URL") or f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Ensure environment variables are correctly configured.")

# Create the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    language = Column(String)
    difficulty = Column(String)

# Create the database tables
def create_user_table():
    """
    Create the user table in the PostgreSQL database if it doesn't exist.
    """
    try:
        # Create tables if they do not exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        if "users" not in existing_tables:
            Base.metadata.create_all(bind=engine)
            print("User table created.")
        else:
            print("User table already exists.")
    except Exception as e:
        print(f"Failed to create table: {e}")

def add_user(db: Session, name: str, email: str, language: str, difficulty: str):
    """
    Add a new user to the PostgreSQL database.

    Args:
        name (str): The user's name.
        email (str): The user's email address.
        language (str): The user's desired programming language.
        difficulty (str): The user's desired difficulty level.
    """
    try:
        user = User(name=name, email=email, language=language, difficulty=difficulty)
        db.add(user)
        db.commit()
        db.refresh(user)
        print("User added successfully.")
    except Exception as e:
        db.rollback()
        print(f"Failed to add user: {e}")

def fetch_users(db: Session) -> list:
    """
    Fetch all registered users from the PostgreSQL database.

    Returns:
        list: A list of user objects.
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        print(f"Failed to fetch users: {e}")
        return []

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.
    
    Yields:
        Session: A SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    create_user_table()
