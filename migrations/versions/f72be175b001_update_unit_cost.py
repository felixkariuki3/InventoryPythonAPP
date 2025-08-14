"""Update unit_cost

Revision ID: f72be175b001
Revises: 22362a3d5007
Create Date: 2025-08-14 11:28:55.544009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f72be175b001'
down_revision: Union[str, Sequence[str], None] = '22362a3d5007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
