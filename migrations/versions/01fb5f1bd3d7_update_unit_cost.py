"""Update unit_cost

Revision ID: 01fb5f1bd3d7
Revises: f72be175b001
Create Date: 2025-08-14 11:32:01.177063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01fb5f1bd3d7'
down_revision: Union[str, Sequence[str], None] = 'f72be175b001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
