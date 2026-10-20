
"""add user token version

Revision ID: fc001d3b4d06
Revises: 3d239667505b
Create Date: 2026-10-20 05:48:17.890727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fc001d3b4d06'
down_revision: Union[str, None] = '3d239667505b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "token_version",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
    )

def downgrade() -> None:
    op.drop_column("users", "token_version")
