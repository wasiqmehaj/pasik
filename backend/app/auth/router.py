from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import OTPRequest, OTPVerify
from app.auth.service import send_otp, verify_otp, create_access_token, get_current_user
from database import get_db
from models import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/otp/request")
def request_otp(payload: OTPRequest):
    send_otp(payload.phone)
    return {"message": "OTP sent successfully"}

@router.post("/otp/verify")
def verify_otp_endpoint(payload: OTPVerify, db: Session = Depends(get_db)):
    if not verify_otp(payload.phone, payload.code):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(User).filter(User.phone == payload.phone).first()
    if user is None:
        user = User(phone=payload.phone, name="New User")
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(payload.phone)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(phone: str = Depends(get_current_user)):
    return {"phone": phone}
