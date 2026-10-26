import uuid

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ProjectPartner(Base):
    """Perspektif Partner: partner yang terlibat di project beserta perannya,
    misalnya Principal: Zabbix SIA, Vendor: PT Bangunindo Teknusa."""

    __tablename__ = "project_partners"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    )
    partner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("partners.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    )
    partner_role: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        default="Partner",
        server_default=text("'Partner'"),
    )

    project = relationship("Project", back_populates="partners", lazy="raise")
    partner = relationship("Partner", lazy="raise")
