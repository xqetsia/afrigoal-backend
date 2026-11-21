from functools import cache

import firebase_admin
from fastapi import Header, HTTPException
from firebase_admin import auth, credentials

from app.config import FIREBASE_CREDENTIALS_PATH


# Initialized on first use, not at import, so tests and CI can import the app
# without a service-account.json. @cache makes it run only once.
@cache
def _firebase_app():
    return firebase_admin.initialize_app(credentials.Certificate(FIREBASE_CREDENTIALS_PATH))


# Plain def: verify_id_token is blocking, so FastAPI runs this in the threadpool.
def get_current_user(authorization: str | None = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.removeprefix("Bearer ")

    try:
        return auth.verify_id_token(token, app=_firebase_app())
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
