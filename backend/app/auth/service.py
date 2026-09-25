import random
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# Temporary in-memory store: { phone: otp_code }
# This will later be replaced by a database table or Redis.
otp_store = {}

# --- JWT settings ---
# NOTE: this secret is fine for local dev only. Before going live, move it
# into your .env file and load it from there instead of hardcoding it.
SECRET_KEY = "dev-secret-change-me-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # token valid for 7 days


def generate_otp() -> str:
    """Generates a 6-digit OTP as a string."""
    return str(random.randint(100000, 999999))


def send_otp(phone: str) -> str:
    """
    Fake OTP sender for local development.
    Stores the OTP in memory so it can be verified later.
    """
    otp = generate_otp()
    otp_store[phone] = otp
    print(f"[FAKE SMS] Sending OTP {otp} to {phone}")
    return otp


def verify_otp(phone: str, code: str) -> bool:
    """
    Checks if the code matches what was sent for this phone.
    Removes the OTP after a successful check (one-time use).
    """
    correct_code = otp_store.get(phone)
    if correct_code is not None and correct_code == code:
        del otp_store[phone]
        return True
    return False


def create_access_token(phone: str) -> str:
    """
    Creates a signed JWT for a verified user.
    The token contains the phone number and an expiry time.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": phone, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    """
    Decodes the JWT from the request's Authorization header.
    Returns the phone number if valid, otherwise rejects the request.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
        return phone
    except JWTError:
        raise credentials_exception