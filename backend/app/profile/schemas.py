from pydantic import BaseModel, field_validator
from typing import Optional


class ProfileUpdateRequest(BaseModel):
    name: str
    nickname: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ProfileResponse(BaseModel):
    id: str
    phone: str
    name: str
    nickname: Optional[str] = None
    active_role: str
    profile_complete: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


class RoleUpdateRequest(BaseModel):
    active_role: str

    @field_validator("active_role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ("buyer", "seller"):
            raise ValueError('active_role must be either "buyer" or "seller"')
        return v