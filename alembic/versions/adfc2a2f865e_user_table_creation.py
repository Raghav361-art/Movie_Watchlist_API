"""user table creation

Revision ID: adfc2a2f865e
Revises: 272c7b569b71
Create Date: 2026-09-04 09:47:20.165031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adfc2a2f865e'
down_revision: Union[str, Sequence[str], None] = '272c7b569b71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",

        sa.Column(
            "id",
            sa.INTEGER(),
            autoincrement=True,
            nullable=False
        ),

        sa.Column(
            "email",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "password",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()")
        ),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )


def downgrade():
    op.drop_table("users")
