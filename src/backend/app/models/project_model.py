import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Project(Base):
    """Perspektif Project. Satu baris = satu portofolio; perspektif lain menempel lewat project_id."""

    __tablename__ = "projects"

    __table_args__ = (
        CheckConstraint(
            "end_date >= start_date",
            name="ck_projects_dates_order",
        ),
        CheckConstraint(
            "value_before_tax >= 0",
            name="ck_projects_value_before_tax_non_negative",
        ),
        CheckConstraint(
            "carry_over_value IS NULL OR carry_over_value >= 0",
            name="ck_projects_carry_over_value_non_negative",
        ),
        Index("ix_projects_status_year", "project_status_id", "project_year"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    # "Project ID" di Excel, contoh ITMS_MON_BMRI_2026_PRO. Unik, dipakai sebagai kunci impor.
    project_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    project_name: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )
    opportunity: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )
    project_year: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    contract_po_name: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )
    contract_po_number: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )
    business_unit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business_units.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    project_status_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_statuses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    value_before_tax: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )
    carry_over_value: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
    )
    project_manager: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )
    account_manager: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    project_objective: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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

    customer = relationship("Customer", back_populates="projects", lazy="raise")
    business_unit = relationship("BusinessUnit", lazy="raise")
    project_status = relationship("ProjectStatus", lazy="raise")
    financial = relationship(
        "ProjectFinancial",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="raise",
    )
    products = relationship(
        "ProjectProduct",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="raise",
    )
    tech_stacks = relationship(
        "ProjectTechStack",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="raise",
    )
    partners = relationship(
        "ProjectPartner",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="raise",
    )
