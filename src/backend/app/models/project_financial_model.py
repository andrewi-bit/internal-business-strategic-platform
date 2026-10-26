import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ProjectFinancial(Base):
    """Perspektif Financial (1:1 dengan project). Net profit = revenue - cogs - operational_costs,
    dihitung saat dibaca supaya tidak pernah tidak sinkron."""

    __tablename__ = "project_financials"

    __table_args__ = (
        CheckConstraint(
            "revenue >= 0 AND cogs >= 0 AND operational_costs >= 0",
            name="ck_project_financials_amounts_non_negative",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    revenue: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )
    cogs: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
    )
    operational_costs: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=Decimal("0"),
        server_default=text("0"),
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

    project = relationship("Project", back_populates="financial", lazy="raise")
