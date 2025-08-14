"""Update unit_cost

Revision ID: 2fe973e19d04
Revises: 0c48c698f6c5
Create Date: 2025-08-14 15:01:14.807844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fe973e19d04'
down_revision: Union[str, Sequence[str], None] = '0c48c698f6c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("inventory_transactions") as batch_op:
        batch_op.add_column(sa.Column("unit_cost", sa.Float(), nullable=True))

    with op.batch_alter_table("transactions") as batch_op:
        batch_op.add_column(sa.Column("unit_cost", sa.Float(), nullable=True))

def downgrade():
    with op.batch_alter_table("inventory_transactions") as batch_op:
        batch_op.drop_column("unit_cost")
    
    with op.batch_alter_table("transactions") as batch_op:
        batch_op.drop_column("unit_cost")

