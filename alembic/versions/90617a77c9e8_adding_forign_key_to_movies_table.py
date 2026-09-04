"""adding forign key to movies table

Revision ID: 90617a77c9e8
Revises: adfc2a2f865e
Create Date: 2026-09-04 09:54:42.350466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90617a77c9e8'
down_revision: Union[str, Sequence[str], None] = 'adfc2a2f865e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("movies", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("movie_user_id_fkey", "movies", "users", ['user_id'], ['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("movie_user_id_fkey", "movies")
    op.drop_column("movies", "user_id")

    """Downgrade schema."""
    pass
