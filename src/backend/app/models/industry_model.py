import uuid

from sqlalchemy import Boolean, Index, SmallInteger, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Industry(Base):
    __tablename__ = "industries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    industry_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    industry_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    industry_description: Mapped[str | None] = mapped_column(
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
    "uq_industries_industry_name_lower",
    func.lower(Industry.industry_name),
    unique=True,
)
