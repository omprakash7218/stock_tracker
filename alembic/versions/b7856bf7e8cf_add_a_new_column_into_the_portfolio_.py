"""add a new column into the portfolio table of db

Revision ID: b7856bf7e8cf
Revises: dd1e009f777
Create Date: 2026-07-28 07:32:46.805675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7856bf7e8cf'
down_revision: Union[str, Sequence[str], None] = 'dd1e009f777'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('portfolios',sa.Column('balance',sa.Float(), nullable= False,server_default='0.0')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'portfolios','balance'
    )
