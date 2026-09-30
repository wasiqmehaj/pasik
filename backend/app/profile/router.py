from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.auth.service import get_current_user
from app.profile.schemas import ProfileUpdateRequest, ProfileResponse, RoleUpdateRequest
from app.profile.service import (
    get_user_by_phone,
    update_profile,
    update_active_role,
    user_to_profile_response,
)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=ProfileResponse)
def read_my_profile(
    phone: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = get_user_by_phone(db, phone)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_profile_response(user)


@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    payload: ProfileUpdateRequest,
    phone: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user = update_profile(db, phone, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_profile_response(user)


@router.patch("/role", response_model=ProfileResponse)
def switch_role(
    payload: RoleUpdateRequest,
    phone: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user = update_active_role(db, phone, payload.active_role)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_profile_response(user)