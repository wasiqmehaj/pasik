from typing import Optional
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement

from models import User
from app.profile.schemas import ProfileUpdateRequest, ProfileResponse


def get_user_by_phone(db: Session, phone: str) -> Optional[User]:
    """Fetches a user row by phone number."""
    return db.query(User).filter(User.phone == phone).first()


def _point_to_latlng(geom) -> tuple[Optional[float], Optional[float]]:
    """
    Converts a stored PostGIS Geometry column value into (latitude, longitude).
    Returns (None, None) if no location is set.
    """
    if geom is None:
        return None, None
    point = to_shape(geom)  # shapely Point
    return point.y, point.x  # y = latitude, x = longitude


def _latlng_to_point(lat: float, lng: float) -> WKTElement:
    """Converts latitude/longitude floats into a PostGIS-compatible WKT point."""
    return WKTElement(f"POINT({lng} {lat})", srid=4326)


def user_to_profile_response(user: User) -> ProfileResponse:
    """Converts a User ORM object into a ProfileResponse, handling the geometry conversion."""
    lat, lng = _point_to_latlng(user.location)
    return ProfileResponse(
        id=str(user.id),
        phone=user.phone,
        name=user.name,
        nickname=user.nickname,
        active_role=user.active_role,
        profile_complete=user.profile_complete,
        latitude=lat,
        longitude=lng,
    )


def update_profile(db: Session, phone: str, payload: ProfileUpdateRequest) -> User:
    """
    Updates the current user's profile fields.
    Marks profile_complete = True once name is set (location is optional at this stage).
    """
    user = get_user_by_phone(db, phone)
    if user is None:
        raise ValueError("User not found")

    user.name = payload.name
    user.nickname = payload.nickname

    if payload.latitude is not None and payload.longitude is not None:
        user.location = _latlng_to_point(payload.latitude, payload.longitude)

    user.profile_complete = True

    db.commit()
    db.refresh(user)
    return user


def update_active_role(db: Session, phone: str, new_role: str) -> User:
    """Updates the user's active buyer/seller role."""
    user = get_user_by_phone(db, phone)
    if user is None:
        raise ValueError("User not found")

    user.active_role = new_role
    db.commit()
    db.refresh(user)
    return user