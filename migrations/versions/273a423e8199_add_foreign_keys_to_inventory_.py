"""Add foreign keys to inventory transactions

Revision ID: 273a423e8199
Revises: 584829e655bc
Create Date: 2025-08-12 13:42:01.470184
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision: str = '273a423e8199'
down_revision: Union[str, Sequence[str], None] = '584829e655bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # If work_in_progress exists, drop it safely
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'work_in_progress' in inspector.get_table_names():
        with op.batch_alter_table('work_in_progress', schema=None) as batch_op:
            idx_names = [idx['name'] for idx in inspector.get_indexes('work_in_progress')]
            if 'ix_work_in_progress_id' in idx_names:
                batch_op.drop_index('ix_work_in_progress_id')
        op.drop_table('work_in_progress')

    # boms table foreign keys
    with op.batch_alter_table('boms', schema=None) as batch_op:
        batch_op.drop_constraint('fk_boms_parent_item_id_items', type_='foreignkey')
        batch_op.drop_constraint('fk_boms_component_item_id_items', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_boms_parent_item_id_items',
            'items',
            ['parent_item_id'],
            ['item_id']
        )
        batch_op.create_foreign_key(
            'fk_boms_component_item_id_items',
            'items',
            ['component_item_id'],
            ['item_id']
        )

    # inventory_logs foreign key
    with op.batch_alter_table('inventory_logs', schema=None) as batch_op:
        batch_op.drop_constraint('fk_inventory_logs_item_id_items', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_inventory_logs_item_id_items',
            'items',
            ['item_id'],
            ['item_id']
        )

    # inventory_transactions foreign key
    with op.batch_alter_table('inventory_transactions', schema=None) as batch_op:
        batch_op.drop_constraint('fk_inventory_transactions_item_id_items', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_inventory_transactions_item_id_items',
            'items',
            ['item_id'],
            ['item_id']
        )

    # items table
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('item_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.create_index('ix_items_item_id', ['item_id'], unique=True)
        batch_op.drop_constraint('fk_items_item_id_items', type_='foreignkey')

    # production_operations table
    with op.batch_alter_table('production_operations', schema=None) as batch_op:
        batch_op.alter_column('order_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # production_orders foreign key
    with op.batch_alter_table('production_orders', schema=None) as batch_op:
        batch_op.alter_column('item_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint('fk_production_orders_item_id_items', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_production_orders_item_id_items',
            'items',
            ['item_id'],
            ['item_id']
        )

    # purchase_order_lines foreign key
    with op.batch_alter_table('purchase_order_lines', schema=None) as batch_op:
        batch_op.drop_constraint('fk_purchase_order_lines_item_id_items', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_purchase_order_lines_item_id_items',
            'items',
            ['item_id'],
            ['item_id']
        )

    # transactions foreign key
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_constraint('fk_transactions_item_id_items', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_transactions_item_id_items',
            'items',
            ['item_id'],
            ['item_id']
        )

    # uom_conversions foreign key
    with op.batch_alter_table('uom_conversions', schema=None) as batch_op:
        batch_op.drop_constraint('fk_uom_conversions_item_id_items', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_uom_conversions_item_id_items',
            'items',
            ['item_id'],
            ['item_id']
        )


def downgrade() -> None:
    """Downgrade schema."""
    # (We’d reverse the changes here — but for now, main focus is fixing the upgrade)
    pass
