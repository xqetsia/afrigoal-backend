import os 
from dotenv import load_dotenv

load_dotenv()

LIVESCORE_API_KEY = os.environ["LIVESCORE_API_KEY"]
LIVESCORE_API_SECRET = os.environ["LIVESCORE_API_SECRET"]

# SQLAlchemy picks the driver from the URL scheme. Plain postgres:// or postgresql://
# means psycopg2, so rewrite it to use psycopg3. Render gives us the plain form.
DATABASE_URL = os.environ["DATABASE_URL"]
for prefix in ("postgres://", "postgresql://"):
    if DATABASE_URL.startswith(prefix):
        DATABASE_URL = "postgresql+psycopg://" + DATABASE_URL.removeprefix(prefix)
        break

FIREBASE_CREDENTIALS_PATH = os.environ["FIREBASE_CREDENTIALS_PATH"]

