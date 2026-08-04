"""add symbol column to trades backfilled from assets

Revision ID: 8ead55516675
Revises: 1ea683585354
Create Date: 2026-07-28 08:21:52.503919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ead55516675'
down_revision: Union[str, Sequence[str], None] = '1ea683585354'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step A: add the column as nullable first (safe — no data yet)
    op.add_column('trades', sa.Column('symbol', sa.String(), nullable=True))

    # Step B: backfill — copy symbol from assets table using the asset_id link
    connection = op.get_bind()
    connection.execute(sa.text(
        """
        UPDATE trades
        SET symbol = assets.symbol
        FROM assets
        WHERE trades.asset_id = assets.id
        """
    ))

    # Step C: now that every row has a symbol, lock it down as NOT NULL
    op.alter_column('trades', 'symbol', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('trades', 'symbol')