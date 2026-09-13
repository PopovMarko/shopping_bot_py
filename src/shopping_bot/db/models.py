from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Enum, ForeignKey, String, false
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship as sa_relationship

from shopping_bot.core.records.utils import RequestStatus


class Base(DeclarativeBase):
    pass


def relationship(*args, **kwargs):
    kwargs.setdefault("lazy", "selectin")
    return sa_relationship(*args, **kwargs)


class ProductModel(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    unit: Mapped[str]
    requests: Mapped[list[RequestModel]] = relationship(
        "RequestModel", back_populates="product", foreign_keys="RequestModel.product_id"
    )


class StoreModel(Base):
    __tablename__ = "stores"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address: Mapped[str]


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(50))
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=false())
    shopping_status: Mapped[bool] = mapped_column(default=False, server_default=false())
    active_message_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    shopping_started_at: Mapped[datetime | None]

    requests: Mapped[list[RequestModel]] = relationship(
        "RequestModel",
        back_populates="requested_by_user",
        foreign_keys="RequestModel.requested_by_user_id",
    )


class RequestModel(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    requested_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    requested_quantity: Mapped[Decimal]
    requested_at: Mapped[datetime]
    receipt_id: Mapped[int | None] = mapped_column(
        ForeignKey("receipts.id"), nullable=True
    )
    price: Mapped[Decimal | None]
    quantity: Mapped[Decimal | None]
    match_confidence: Mapped[int | None]
    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus, name="request_status_constraint"),
        default=RequestStatus.pending,
    )

    product: Mapped[ProductModel] = relationship(
        "ProductModel", foreign_keys=product_id
    )
    requested_by_user: Mapped[UserModel] = relationship(
        "UserModel", foreign_keys=requested_by_user_id
    )


class ReceiptModel(Base):
    __tablename__ = "receipts"
    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=True)
    uploaded_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receipt_date: Mapped[datetime]
    image_url: Mapped[str | None]
    raw_model_response: Mapped[str | None]
    created_at: Mapped[datetime]
