import uuid

from sqlalchemy import Boolean, CheckConstraint, Index, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TechStack(Base):
    __tablename__ = "tech_stacks"

    __table_args__ = (
        CheckConstraint(
            "tech_stack_category IN ('frontend', 'backend', 'data_storage')",
            name="ck_tech_stacks_category",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    tech_stack_category: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    tech_stack_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )


Index(
    "uq_tech_stacks_category_name_lower",
    TechStack.tech_stack_category,
    func.lower(TechStack.tech_stack_name),
    unique=True,
)
