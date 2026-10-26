import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Customer(Base):
    """Perspektif Customer pada portofolio (satu customer bisa punya banyak project)."""

    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    customer_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    company_size_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("company_sizes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    # Kolom "Revenue/Annual Sales/Annual Budget" di Excel berupa teks bebas,
    # misalnya "115T (FY 2025)", jadi tidak disimpan sebagai angka.
    annual_revenue: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    customer_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customer_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    industry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("industries.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    location: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )
    legal_structure_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("legal_structures.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    company_size = relationship("CompanySize", lazy="raise")
    customer_type = relationship("CustomerType", lazy="raise")
    industry = relationship("Industry", lazy="raise")
    legal_structure = relationship("LegalStructure", lazy="raise")
    projects = relationship("Project", back_populates="customer", lazy="raise")


Index(
    "uq_customers_customer_name_lower",
    func.lower(Customer.customer_name),
    unique=True,
)
