import os 
from dotenv import load_dotenv

load_dotenv()

LIVESCORE_API_KEY = os.environ["LIVESCORE_API_KEY"]
LIVESCORE_API_SECRET = os.environ["LIVESCORE_API_SECRET"]
DATABASE_URL = os.environ["DATABASE_URL"]
FIREBASE_CREDENTIALS_PATH = os.environ["FIREBASE_CREDENTIALS_PATH"]

