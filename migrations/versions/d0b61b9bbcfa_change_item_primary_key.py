"""change item primary key

Revision ID: d0b61b9bbcfa
Revises: 25f7324b8cc6
Create Date: 2025-08-18 11:00:35.080719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0b61b9bbcfa'
down_revision: Union[str, Sequence[str], None] = '25f7324b8cc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop old FK (assuming it was named fk_purchase_order_lines_item_id before)
    op.drop_constraint('fk_purchase_order_lines_item_id', 'purchase_order_lines', type_='foreignkey')
    
    # Create new FK to items.item_id
    op.create_foreign_key(
        'fk_purchase_order_lines_item_id',    # new constraint name
        'purchase_order_lines',              # source table
        'items',                             # target table
        ['item_id'],                         # local column
        ['item_id']                          # remote column
    )

def downgrade():
    # Drop new FK
    op.drop_constraint('fk_purchase_order_lines_item_id', 'purchase_order_lines', type_='foreignkey')
    
    # Restore old FK (if it was pointing to items.id before)
    op.create_foreign_key(
        'fk_purchase_order_lines_item_id',
        'purchase_order_lines',
        'items',
        ['item_id'],
        ['id']   # <-- restore old reference if you ever downgrade
    )