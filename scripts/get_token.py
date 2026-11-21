"""Print a real Firebase ID token for manual testing of protected routes.

Dev tool only. Never expose this as an endpoint.

Usage:
    python scripts/get_token.py              # uid "dev-test-user"
    python scripts/get_token.py some-uid
    curl -H "Authorization: Bearer $(python scripts/get_token.py)" localhost:8000/me/teams

Needs in .env: FIREBASE_CREDENTIALS_PATH and FIREBASE_WEB_API_KEY
(Firebase Console > Project settings > General > Web API key).
"""
import os
import sys

import firebase_admin
import httpx
from dotenv import load_dotenv
from firebase_admin import auth, credentials

load_dotenv()

uid = sys.argv[1] if len(sys.argv) > 1 else "dev-test-user"

# 1. Admin SDK signs a custom token for this uid using the service account.
firebase_admin.initialize_app(credentials.Certificate(os.environ["FIREBASE_CREDENTIALS_PATH"]))
custom_token = auth.create_custom_token(uid).decode()

# 2. Firebase exchanges it for an ID token, the same kind the iOS app sends. Valid 1 hour.
response = httpx.post(
    "https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken",
    params={"key": os.environ["FIREBASE_WEB_API_KEY"]},
    json={"token": custom_token, "returnSecureToken": True},
)
if response.is_error:
    sys.exit(f"Firebase error {response.status_code}: {response.json().get('error', {}).get('message')}")

print(response.json()["idToken"])
