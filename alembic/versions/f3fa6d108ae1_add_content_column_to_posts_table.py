"""add content column to posts table

Revision ID: f3fa6d108ae1
Revises: 14375519a104
Create Date: 2026-09-05 22:41:08.747204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3fa6d108ae1'
down_revision: Union[str, Sequence[str], None] = '14375519a104'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
