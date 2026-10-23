import uuid

from sqlalchemy import ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    product_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    product_status_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_statuses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )


Index(
    "uq_products_product_name_lower",
    func.lower(Product.product_name),
    unique=True,
)
