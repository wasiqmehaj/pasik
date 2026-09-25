from pydantic import BaseModel, Field

class OTPRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, description="User's phone number")

class OTPVerify(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)
    code: str = Field(..., min_length=6, max_length=6)