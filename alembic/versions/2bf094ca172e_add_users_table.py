"""add users table

Revision ID: 2bf094ca172e
Revises: f3fa6d108ae1
Create Date: 2026-09-05 22:51:29.491154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bf094ca172e'
down_revision: Union[str, Sequence[str], None] = 'f3fa6d108ae1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column("password", sa.String(), nullable=False),
            sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                      server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email")
            )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
