"""adding new column

Revision ID: 272c7b569b71
Revises: ab398b7b2e9f
Create Date: 2026-09-04 08:59:03.133696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '272c7b569b71'
down_revision: Union[str, Sequence[str], None] = 'ab398b7b2e9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "movies",
        sa.Column("director", sa.String(), nullable=False)
    )

    op.add_column(
        "movies",
        sa.Column("genre", sa.String(), nullable=False)
    )

    op.add_column(
        "movies",
        sa.Column("release_year", sa.INTEGER(), nullable=False)
    )

    op.add_column(
        "movies",
        sa.Column(
            "watched",
            sa.BOOLEAN(),
            nullable=False,
            server_default="false"
        )
    )

    op.add_column(
        "movies",
        sa.Column("rating", sa.INTEGER())
    )

    op.add_column(
        "movies",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()")
        )
    )

    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column("movies", "created_at")
    op.drop_column("movies", "rating")
    op.drop_column("movies", "watched")
    op.drop_column("movies", "release_year")
    op.drop_column("movies", "genre")
    op.drop_column("movies", "director")
    """Downgrade schema."""
    pass
