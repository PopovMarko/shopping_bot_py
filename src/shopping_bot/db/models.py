from __future__ import annotations

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Enum, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RequestStatus(str, enum.Enum):
    pending = "pending"
    fulfilled = "fulfilled"
    cancelled = "cancelled"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(50))
    shopping_status: Mapped[bool]
    active_message_id: Mapped[int] = mapped_column(BigInteger)
    shopping_started_at: Mapped[datetime]
    purchases: Mapped[list[Purchase]] = relationship(back_populates="user")
    requests: Mapped[list[Request]] = relationship(back_populates="user")


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    unit: Mapped[str]


class Store(Base):
    __tablename__ = "stores"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address: Mapped[str]


class Request(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    requested_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    requested_quantity: Mapped[Decimal]
    requested_at: Mapped[datetime]
    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus, name="request_status_constraint"),
        default=RequestStatus.pending,
    )
    user: Mapped[User] = relationship(back_populates="requests")


class Receipt(Base):
    __tablename__ = "receipts"
    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    uploaded_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receipt_date: Mapped[datetime]
    image_url: Mapped[str | None]
    raw_model_response: Mapped[str | None]
    created_at: Mapped[datetime]


class Purchase(Base):
    __tablename__ = "purchases"
    id: Mapped[int] = mapped_column(primary_key=True)
    purchased_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    request_id: Mapped[int | None] = mapped_column(ForeignKey("requests.id"))
    receipt_id: Mapped[int | None] = mapped_column(ForeignKey("receipts.id"))
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    price: Mapped[Decimal]
    quantity: Mapped[Decimal]
    purchased_at: Mapped[datetime]
    match_confidence: Mapped[Decimal]
    user: Mapped[User] = relationship(back_populates="purchases")
