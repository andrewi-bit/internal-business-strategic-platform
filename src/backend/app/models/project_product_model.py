import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ProjectProduct(Base):
    """Perspektif Tech Stack, bagian "Product Use": produk apa saja yang dipakai project."""

    __tablename__ = "project_products"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    )

    project = relationship("Project", back_populates="products", lazy="raise")
    product = relationship("Product", lazy="raise")
