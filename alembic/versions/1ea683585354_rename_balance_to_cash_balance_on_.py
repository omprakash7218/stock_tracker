"""rename balance to cash_balance on portfolios

Revision ID: 1ea683585354
Revises: b7856bf7e8cf
Create Date: 2026-07-28 08:12:50.421242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ea683585354'
down_revision: Union[str, Sequence[str], None] = 'b7856bf7e8cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('portfolios', 'balance', new_column_name='cash_balance')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('portfolios','cash_balance',new_column_name='balance')
