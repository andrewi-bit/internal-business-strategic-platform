import uuid

from sqlalchemy import Boolean, Index, SmallInteger, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class BusinessUnit(Base):
    __tablename__ = "business_units"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    business_unit_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    business_unit_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    business_unit_description: Mapped[str | None] = mapped_column(
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
    "uq_business_units_business_unit_name_lower",
    func.lower(BusinessUnit.business_unit_name),
    unique=True,
)
