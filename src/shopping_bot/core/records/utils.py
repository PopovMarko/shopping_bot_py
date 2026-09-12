import enum


class RequestStatus(str, enum.Enum):
    pending = "pending"
    in_cart = "in_cart"
    fulfilled = "fulfilled"
    cancelled = "cancelled"
