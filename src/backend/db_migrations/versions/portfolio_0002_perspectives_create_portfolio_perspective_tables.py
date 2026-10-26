"""create portfolio perspective tables: customers, projects, financials, products, tech stacks and partners

Revision ID: portfolio_0002_perspectives
Revises: portfolio_0001_master
Create Date: 2026-10-25 21:00:00.000000

Satu portofolio = satu baris di projects. Tiap perspektif punya tabel sendiri dan terhubung lewat
foreign key:

    Customer   -> customers            (projects.customer_id -> customers.id)
    Project    -> projects
    Financial  -> project_financials   (project_id, 1:1)
    Tech Stack -> project_products     (Product Use)
                  project_tech_stacks  (Frontend, Backend, Data & Storage)
    Partner    -> project_partners     (project_id + partner_id + role)

Nilai turunan di Excel (value after tax, progress, total/remaining days, net profit) tidak disimpan,
dihitung saat dibaca.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "portfolio_0002_perspectives"
down_revision: Union[str, None] = "portfolio_0001_master"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _uuid_pk(name: str = "id") -> sa.Column:
    return sa.Column(name, postgresql.UUID(as_uuid=True), nullable=False)


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    ]


def _audit_columns() -> list[sa.Column]:
    return [
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["updated_by"], ["users.id"], ondelete="SET NULL"),
    ]


def upgrade() -> None:
    # ---- Customer perspective -------------------------------------------------
    op.create_table(
        "customers",
        _uuid_pk(),
        sa.Column("customer_name", sa.String(length=200), nullable=False),
        sa.Column("company_size_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("annual_revenue", sa.String(length=100), nullable=True),
        sa.Column("customer_type_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("industry_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=True),
        sa.Column("legal_structure_id", postgresql.UUID(as_uuid=True), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(["company_size_id"], ["company_sizes.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["customer_type_id"], ["customer_types.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["industry_id"], ["industries.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["legal_structure_id"], ["legal_structures.id"], ondelete="RESTRICT"),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_customers_customer_name_lower", "customers", [sa.text("lower(customer_name)")], unique=True)
    op.create_index("ix_customers_company_size_id", "customers", ["company_size_id"])
    op.create_index("ix_customers_customer_type_id", "customers", ["customer_type_id"])
    op.create_index("ix_customers_industry_id", "customers", ["industry_id"])
    op.create_index("ix_customers_legal_structure_id", "customers", ["legal_structure_id"])

    # ---- Project perspective --------------------------------------------------
    op.create_table(
        "projects",
        _uuid_pk(),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_code", sa.String(length=100), nullable=False),
        sa.Column("project_name", sa.String(length=250), nullable=False),
        sa.Column("opportunity", sa.String(length=250), nullable=True),
        sa.Column("project_year", sa.SmallInteger(), nullable=False),
        sa.Column("contract_po_name", sa.String(length=250), nullable=True),
        sa.Column("contract_po_number", sa.String(length=150), nullable=True),
        sa.Column("business_unit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_status_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("value_before_tax", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("carry_over_value", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("project_manager", sa.String(length=150), nullable=True),
        sa.Column("account_manager", sa.String(length=150), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("project_objective", sa.Text(), nullable=True),
        *_timestamps(),
        sa.CheckConstraint("end_date >= start_date", name="ck_projects_dates_order"),
        sa.CheckConstraint("value_before_tax >= 0", name="ck_projects_value_before_tax_non_negative"),
        sa.CheckConstraint(
            "carry_over_value IS NULL OR carry_over_value >= 0",
            name="ck_projects_carry_over_value_non_negative",
        ),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["business_unit_id"], ["business_units.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["project_status_id"], ["project_statuses.id"], ondelete="RESTRICT"),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_code"),
    )
    op.create_index("ix_projects_customer_id", "projects", ["customer_id"])
    op.create_index("ix_projects_business_unit_id", "projects", ["business_unit_id"])
    op.create_index("ix_projects_project_status_id", "projects", ["project_status_id"])
    op.create_index("ix_projects_status_year", "projects", ["project_status_id", "project_year"])

    # ---- Financial perspective (1:1 with project) -------------------------------
    op.create_table(
        "project_financials",
        _uuid_pk(),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("revenue", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("cogs", sa.Numeric(precision=18, scale=2), server_default=sa.text("0"), nullable=False),
        sa.Column(
            "operational_costs",
            sa.Numeric(precision=18, scale=2),
            server_default=sa.text("0"),
            nullable=False,
        ),
        *_timestamps(),
        sa.CheckConstraint(
            "revenue >= 0 AND cogs >= 0 AND operational_costs >= 0",
            name="ck_project_financials_amounts_non_negative",
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id"),
    )

    # ---- Tech Stack perspective -------------------------------------------------
    op.create_table(
        "project_products",
        _uuid_pk("project_id"),
        _uuid_pk("product_id"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("project_id", "product_id"),
    )
    op.create_index("ix_project_products_product_id", "project_products", ["product_id"])

    op.create_table(
        "project_tech_stacks",
        _uuid_pk("project_id"),
        _uuid_pk("tech_stack_id"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tech_stack_id"], ["tech_stacks.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("project_id", "tech_stack_id"),
    )
    op.create_index("ix_project_tech_stacks_tech_stack_id", "project_tech_stacks", ["tech_stack_id"])

    # ---- Partner perspective ----------------------------------------------------
    op.create_table(
        "project_partners",
        _uuid_pk("project_id"),
        _uuid_pk("partner_id"),
        sa.Column(
            "partner_role",
            sa.String(length=60),
            server_default=sa.text("'Partner'"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["partner_id"], ["partners.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("project_id", "partner_id"),
    )
    op.create_index("ix_project_partners_partner_id", "project_partners", ["partner_id"])


def downgrade() -> None:
    op.drop_index("ix_project_partners_partner_id", table_name="project_partners")
    op.drop_table("project_partners")

    op.drop_index("ix_project_tech_stacks_tech_stack_id", table_name="project_tech_stacks")
    op.drop_table("project_tech_stacks")

    op.drop_index("ix_project_products_product_id", table_name="project_products")
    op.drop_table("project_products")

    op.drop_table("project_financials")

    op.drop_index("ix_projects_status_year", table_name="projects")
    op.drop_index("ix_projects_project_status_id", table_name="projects")
    op.drop_index("ix_projects_business_unit_id", table_name="projects")
    op.drop_index("ix_projects_customer_id", table_name="projects")
    op.drop_table("projects")

    op.drop_index("ix_customers_legal_structure_id", table_name="customers")
    op.drop_index("ix_customers_industry_id", table_name="customers")
    op.drop_index("ix_customers_customer_type_id", table_name="customers")
    op.drop_index("ix_customers_company_size_id", table_name="customers")
    op.drop_index("uq_customers_customer_name_lower", table_name="customers")
    op.drop_table("customers")
