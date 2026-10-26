import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ProjectTechStack(Base):
    """Perspektif Tech Stack, bagian Frontend / Backend / Data & Storage.
    Kategorinya ikut master tech_stacks.tech_stack_category."""

    __tablename__ = "project_tech_stacks"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tech_stack_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tech_stacks.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    )

    project = relationship("Project", back_populates="tech_stacks", lazy="raise")
    tech_stack = relationship("TechStack", lazy="raise")
