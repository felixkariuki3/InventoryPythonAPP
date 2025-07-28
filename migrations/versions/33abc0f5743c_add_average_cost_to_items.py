"""Add average_cost to items

Revision ID: 33abc0f5743c
Revises: ff3dea3fd50b
Create Date: 2025-07-28 19:35:37.533054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33abc0f5743c'
down_revision: Union[str, Sequence[str], None] = 'ff3dea3fd50b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    with op.batch_alter_table('items') as batch_op:
        batch_op.add_column(sa.Column('average_cost', sa.Float(), nullable=True))


def downgrade():
    with op.batch_alter_table('items') as batch_op:
        batch_op.drop_column('average_cost')