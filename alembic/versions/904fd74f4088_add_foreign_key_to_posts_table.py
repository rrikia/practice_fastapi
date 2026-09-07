"""add foreign-key to posts table

Revision ID: 904fd74f4088
Revises: 2bf094ca172e
Create Date: 2026-09-05 23:04:39.954634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '904fd74f4088'
down_revision: Union[str, Sequence[str], None] = '2bf094ca172e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    # local col is from source table posts, remote cols is from users table
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=[
                          "owner_id"], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
