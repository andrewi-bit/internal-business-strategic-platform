import uuid

from sqlalchemy import Boolean, Index, SmallInteger, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ProductStatus(Base):
    __tablename__ = "product_statuses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    product_status_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    product_status_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    product_status_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    sort_order: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )


Index(
    "uq_product_statuses_product_status_name_lower",
    func.lower(ProductStatus.product_status_name),
    unique=True,
)
