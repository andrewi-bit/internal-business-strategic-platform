"""create portfolio master tables, products, tech stacks and partners

Revision ID: portfolio_0001_master
Revises: f089ebfabb3a
Create Date: 2026-10-22 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "portfolio_0001_master"
down_revision: Union[str, None] = "f089ebfabb3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# (table name, column prefix) for the 7 master tables, which share one structure
MASTER_TABLES = [
    ("company_sizes", "company_size"),
    ("customer_types", "customer_type"),
    ("industries", "industry"),
    ("legal_structures", "legal_structure"),
    ("business_units", "business_unit"),
    ("project_statuses", "project_status"),
    ("product_statuses", "product_status"),
]


def _create_master_table(table_name: str, prefix: str) -> None:
    op.create_table(
        table_name,
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            f"{prefix}_code",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            f"{prefix}_name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            f"{prefix}_description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "sort_order",
            sa.SmallInteger(),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(f"{prefix}_code"),
    )

    op.create_index(
        f"uq_{table_name}_{prefix}_name_lower",
        table_name,
        [sa.text(f"lower({prefix}_name)")],
        unique=True,
    )


def upgrade() -> None:
    for table_name, prefix in MASTER_TABLES:
        _create_master_table(table_name, prefix)

    op.create_table(
        "products",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "product_name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "product_description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "product_status_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["product_status_id"],
            ["product_statuses.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_products_product_name_lower",
        "products",
        [sa.text("lower(product_name)")],
        unique=True,
    )
    op.create_index(
        "ix_products_product_status_id",
        "products",
        ["product_status_id"],
    )

    op.create_table(
        "tech_stacks",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "tech_stack_category",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "tech_stack_name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "tech_stack_category IN ('frontend', 'backend', 'data_storage')",
            name="ck_tech_stacks_category",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_tech_stacks_category_name_lower",
        "tech_stacks",
        ["tech_stack_category", sa.text("lower(tech_stack_name)")],
        unique=True,
    )

    op.create_table(
        "partners",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "partner_name",
            sa.String(length=200),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_partners_partner_name_lower",
        "partners",
        [sa.text("lower(partner_name)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_partners_partner_name_lower", table_name="partners")
    op.drop_table("partners")

    op.drop_index("uq_tech_stacks_category_name_lower", table_name="tech_stacks")
    op.drop_table("tech_stacks")

    op.drop_index("ix_products_product_status_id", table_name="products")
    op.drop_index("uq_products_product_name_lower", table_name="products")
    op.drop_table("products")

    for table_name, prefix in reversed(MASTER_TABLES):
        op.drop_index(f"uq_{table_name}_{prefix}_name_lower", table_name=table_name)
        op.drop_table(table_name)
