"""any peding updates

Revision ID: 25f7324b8cc6
Revises: 9011ff7a6eee
Create Date: 2025-08-14 17:55:32.794554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25f7324b8cc6'
down_revision: Union[str, Sequence[str], None] = '9011ff7a6eee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.add_column(sa.Column('unit_cost', sa.Numeric(12, 2), nullable=True))
    
    with op.batch_alter_table("inventory_transactions", schema=None) as batch_op:
        batch_op.add_column(sa.Column('unit_cost', sa.Numeric(12, 2), nullable=True))
 

 

def downgrade():
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.drop_column('unit_cost')

    with op.batch_alter_table("inventory_transactions", schema=None) as batch_op:
        batch_op.drop_column('unit_cost')