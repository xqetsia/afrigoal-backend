import os 
from dotenv import load_dotenv

load_dotenv()

LIVESCORE_API_KEY = os.getenv("LIVESCORE_API_KEY")
LIVESCORE_API_SECRET = os.getenv("LIVESCORE_API_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")

