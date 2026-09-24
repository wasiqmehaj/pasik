from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
import enum
from datetime import datetime
from database import Base


class UserRole(str, enum.Enum):
    seller = "seller"
    buyer = "buyer"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ItemStatus(str, enum.Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    media_url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)
    status = Column(Enum(ItemStatus), default=ItemStatus.available, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class BidStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Bid(Base):
    __tablename__ = "bids"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    price_quoted = Column(String, nullable=False)
    pickup_datetime = Column(DateTime, nullable=True)
    status = Column(Enum(BidStatus), default=BidStatus.pending, nullable=False)
    otp_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)