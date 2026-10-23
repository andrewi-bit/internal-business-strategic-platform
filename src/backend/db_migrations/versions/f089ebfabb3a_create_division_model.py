
"""create division model and migrate role requests

Revision ID: f089ebfabb3a
Revises: fc001d3b4d06
"""

import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "f089ebfabb3a"
down_revision: Union[str, None] = "fc001d3b4d06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Create the division master table.
    op.create_table(
        "divisions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_divisions_code"),
    )

    connection = op.get_bind()

    # 2. Preserve existing division names as master records.
    existing_divisions = connection.execute(
        sa.text(
            "SELECT DISTINCT division "
            "FROM role_requests ORDER BY division"
        )
    ).scalars().all()

    for division_name in existing_divisions:
        connection.execute(
            sa.text(
                """
                INSERT INTO divisions (id, name, code)
                VALUES (:id, :name, :code)
                """
            ),
            {
                "id": uuid.uuid4(),
                "name": division_name,
                "code": f"legacy-{uuid.uuid4().hex}",
            },
        )

    # 3. Add nullable FK first so existing rows remain valid.
    op.add_column(
        "role_requests",
        sa.Column("division_id", sa.UUID(), nullable=True),
    )

    # 4. Map every existing request to its division record.
    connection.execute(
        sa.text(
            """
            UPDATE role_requests AS rr
            SET division_id = d.id
            FROM divisions AS d
            WHERE d.name = rr.division
            """
        )
    )

    # 5. Enforce integrity after all existing rows are mapped.
    op.alter_column(
        "role_requests",
        "division_id",
        existing_type=sa.UUID(),
        nullable=False,
    )

    op.create_foreign_key(
        "fk_role_requests_division_id_divisions",
        "role_requests",
        "divisions",
        ["division_id"],
        ["id"],
    )

    # 6. Enforce at most one pending request per user.
    op.create_index(
        "uq_role_requests_one_pending_per_user",
        "role_requests",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )

    # 7. Remove the old text field only after mapping succeeds.
    op.drop_column("role_requests", "division")


def downgrade() -> None:
    connection = op.get_bind()

    # Restore the old division field and its values.
    op.add_column(
        "role_requests",
        sa.Column("division", sa.String(150), nullable=True),
    )

    connection.execute(
        sa.text(
            """
            UPDATE role_requests AS rr
            SET division = d.name
            FROM divisions AS d
            WHERE d.id = rr.division_id
            """
        )
    )

    op.alter_column(
        "role_requests",
        "division",
        existing_type=sa.String(150),
        nullable=False,
    )

    op.drop_index(
        "uq_role_requests_one_pending_per_user",
        table_name="role_requests",
    )

    op.drop_constraint(
        "fk_role_requests_division_id_divisions",
        "role_requests",
        type_="foreignkey",
    )

    op.drop_column("role_requests", "division_id")
    op.drop_table("divisions")
