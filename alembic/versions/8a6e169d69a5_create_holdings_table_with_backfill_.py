"""create holdings table with backfill from trades

Revision ID: 8a6e169d69a5
Revises: 8ead55516675
Create Date: 2026-07-28 09:40:48.173039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a6e169d69a5'
down_revision: Union[str, Sequence[str], None] = '8ead55516675'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step A: create the holdings table structure
    op.create_table(
        'holdings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('portfolio_id', sa.Integer(), sa.ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('average_buy_price', sa.Float(), nullable=False),
    )

    # Step B: backfill — aggregate existing BUY trades into weighted-average holdings
    connection = op.get_bind()
    connection.execute(sa.text(
        """
        INSERT INTO holdings (portfolio_id, symbol, quantity, average_buy_price)
        SELECT
            portfolio_id,
            symbol,
            SUM(quantity) AS quantity,
            SUM(quantity * price) / SUM(quantity) AS average_buy_price
        FROM trades
        WHERE trade_type = 'buy'
        GROUP BY portfolio_id, symbol
        """
    ))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('holdings')