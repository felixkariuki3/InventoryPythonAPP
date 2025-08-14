"""Update unit_cost

Revision ID: 0c48c698f6c5
Revises: 31c315fa8492
Create Date: 2025-08-14 11:37:29.017462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c48c698f6c5'
down_revision: Union[str, Sequence[str], None] = '31c315fa8492'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
