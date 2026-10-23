import uuid

from sqlalchemy import Boolean, Index, SmallInteger, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ProjectStatus(Base):
    __tablename__ = "project_statuses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    project_status_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    project_status_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    project_status_description: Mapped[str | None] = mapped_column(
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
    "uq_project_statuses_project_status_name_lower",
    func.lower(ProjectStatus.project_status_name),
    unique=True,
)
