"""initial migration

Revision ID: 19a0ad5cc27a
Revises:
Create Date: 2026-02-26 17:05:15.495772

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "19a0ad5cc27a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new column to user table
    op.add_column("user", sa.Column("hashed_secret_key", sa.String(), nullable=True))

    # Create refresh_token table
    op.create_table(
        "refresh_token",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "user_id", UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=False
        ),
        sa.Column("jti", sa.String(), nullable=False, unique=True),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "revoked", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )


def downgrade() -> None:
    # Drop refresh_token table
    op.drop_table("refresh_token")

    # Drop hashed_secret_key column
    op.drop_column("user", "hashed_secret_key")
