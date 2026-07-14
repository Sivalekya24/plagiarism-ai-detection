"""
Admin authentication core.

No database yet -> a single admin account is defined entirely via
environment variables:

  ADMIN_USERNAME              plain username, e.g. "admin"
  ADMIN_PASSWORD_HASH         bcrypt hash of the password (never the raw
                              password) -- generate it with
                              generate_admin_hash.py in this same folder
  JWT_SECRET_KEY              long random string, e.g. `openssl rand -hex 32`
  ADMIN_TOKEN_EXPIRE_MINUTES  optional, defaults to 120

When you outgrow a single hardcoded admin, swap verify_admin_credentials()
for a real user lookup (DB) -- create_admin_token() / decode_admin_token()
and the require_admin dependency in api/deps.py don't need to change.
"""

import os
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
ADMIN_PASSWORD_HASH = os.environ["ADMIN_PASSWORD_HASH"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(os.environ.get("ADMIN_TOKEN_EXPIRE_MINUTES", "120"))


def _check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def verify_admin_credentials(username: str, password: str) -> bool:
    if username != ADMIN_USERNAME:
        # Run the hash check anyway so a wrong username doesn't return
        # faster than a wrong password -- avoids leaking which one was
        # wrong via response timing.
        _check_password(password, ADMIN_PASSWORD_HASH)
        return False
    return _check_password(password, ADMIN_PASSWORD_HASH)


def create_admin_token() -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": ADMIN_USERNAME, "role": "admin", "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_admin_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError as exc:
        raise ValueError("invalid or expired token") from exc
    if payload.get("role") != "admin":
        raise ValueError("not an admin token")
    return payload
