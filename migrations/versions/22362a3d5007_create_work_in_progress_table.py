"""Create work_in_progress table

Revision ID: 22362a3d5007
Revises: create_wip_table
Create Date: 2025-08-14 11:28:27.255593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22362a3d5007'
down_revision: Union[str, Sequence[str], None] = 'create_wip_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
