"""God with us all

Revision ID: 48f4a6b93cce
Revises: 5755e76ed3ae
Create Date: 2025-08-21 13:51:35.123106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48f4a6b93cce'
down_revision: Union[str, Sequence[str], None] = '5755e76ed3ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create a new temp table with correct foreign key names
    op.create_table(
        'purchase_order_lines_new',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column(
            'order_id', sa.Integer,
            sa.ForeignKey('purchase_orders.id', name="fk_purchase_order_lines_order_id")
        ),
        sa.Column(
            'item_id', sa.Integer,
            sa.ForeignKey('items.item_id', name="fk_purchase_order_lines_item_id")
        ),
        sa.Column('quantity', sa.Float, nullable=False),
        sa.Column('received_qty', sa.Float, server_default="0"),
        sa.Column('unit_cost', sa.Float, nullable=False),
        sa.Column(
            'warehouse_id', sa.Integer,
            sa.ForeignKey('warehouses.id', name="fk_purchase_order_lines_warehouses_id")
        ),
    )

    # Copy data from old table
    op.execute("""
        INSERT INTO purchase_order_lines_new (id, order_id, item_id, quantity, received_qty, unit_cost, warehouse_id)
        SELECT id, order_id, item_id, quantity, received_qty, unit_cost, warehouse_id
        FROM purchase_order_lines
    """)

    # Drop old table and rename new one
    op.drop_table('purchase_order_lines')
    op.rename_table('purchase_order_lines_new', 'purchase_order_lines')


def downgrade():
    # Recreate the old table without explicit constraint names
    op.create_table(
        'purchase_order_lines_old',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('purchase_orders.id')),
        sa.Column('item_id', sa.Integer, sa.ForeignKey('items.item_id')),
        sa.Column('quantity', sa.Float, nullable=False),
        sa.Column('received_qty', sa.Float, server_default="0"),
        sa.Column('unit_cost', sa.Float, nullable=False),
        sa.Column('warehouse_id', sa.Integer, sa.ForeignKey('warehouses.id')),
    )

    op.execute("""
        INSERT INTO purchase_order_lines_old (id, order_id, item_id, quantity, received_qty, unit_cost, warehouse_id)
        SELECT id, order_id, item_id, quantity, received_qty, unit_cost, warehouse_id
        FROM purchase_order_lines
    """)

    op.drop_table('purchase_order_lines')
    op.rename_table('purchase_order_lines_old', 'purchase_order_lines')
