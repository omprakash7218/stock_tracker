"""fix timestamp default"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "dd1e009f777"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ✅ Add default to timestamp column (safe, keeps data)
    op.alter_column(
        "transactions",
        "timestamp",
        server_default=sa.text("CURRENT_TIMESTAMP"),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )


def downgrade() -> None:
    # ✅ Remove default if rollback
    op.alter_column(
        "transactions",
        "timestamp",
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )