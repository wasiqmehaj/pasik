from fastapi import APIRouter
from app.auth.schemas import OTPRequest
from app.auth.service import send_otp

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/otp/request")
def request_otp(payload: OTPRequest):
    send_otp(payload.phone)
    return {"message": "OTP sent successfully"}