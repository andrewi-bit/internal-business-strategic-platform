import uuid

from sqlalchemy import Boolean, Index, SmallInteger, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CompanySize(Base):
    __tablename__ = "company_sizes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    company_size_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    company_size_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    company_size_description: Mapped[str | None] = mapped_column(
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
    "uq_company_sizes_company_size_name_lower",
    func.lower(CompanySize.company_size_name),
    unique=True,
)
