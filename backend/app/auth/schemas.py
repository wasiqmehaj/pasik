from pydantic import BaseModel, Field

class OTPRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, description="User's phone number")