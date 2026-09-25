from fastapi import APIRouter, HTTPException, Depends
from app.auth.schemas import OTPRequest, OTPVerify
from app.auth.service import send_otp, verify_otp, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/otp/request")
def request_otp(payload: OTPRequest):
    send_otp(payload.phone)
    return {"message": "OTP sent successfully"}

@router.post("/otp/verify")
def verify_otp_endpoint(payload: OTPVerify):
    if verify_otp(payload.phone, payload.code):
        token = create_access_token(payload.phone)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

@router.get("/me")
def read_current_user(phone: str = Depends(get_current_user)):
    return {"phone": phone}