"""DB schema updates in batch mode

Revision ID: bcf58907e067
Revises: d0b61b9bbcfa
Create Date: 2025-08-19 15:56:41.425261
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcf58907e067'
down_revision: Union[str, Sequence[str], None] = 'd0b61b9bbcfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema (batch mode)."""

    # boms
    with op.batch_alter_table('boms') as batch_op:
        batch_op.alter_column('quantity',
            existing_type=sa.FLOAT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
    op.create_index(op.f('ix_boms_id'), 'boms', ['id'], unique=False)

    # inventory_logs
    with op.batch_alter_table('inventory_logs') as batch_op:
        batch_op.alter_column('transaction_id',
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column('timestamp',
            existing_type=sa.TIMESTAMP(),
            server_default=None,
            type_=sa.DateTime(),
            existing_nullable=True,
        )
        batch_op.create_foreign_key(
            'fk_inventory_logs_transaction_id',
            'transactions',
            ['transaction_id'],
            ['id']
        )
    op.create_index(op.f('ix_inventory_logs_id'), 'inventory_logs', ['id'], unique=False)

    # inventory_transactions
    with op.batch_alter_table('inventory_transactions') as batch_op:
        batch_op.alter_column('unit_cost',
            existing_type=sa.NUMERIC(precision=12, scale=2),
            type_=sa.Float(),
            existing_nullable=True,
        )
    op.create_index(op.f('ix_inventory_transactions_id'), 'inventory_transactions', ['id'], unique=False)

    # items
    with op.batch_alter_table('items') as batch_op:
        batch_op.alter_column('name',
            existing_type=sa.TEXT(),
            type_=sa.String(),
            existing_nullable=True,
        )
        batch_op.alter_column('item_id',
            existing_type=sa.TEXT(),
            type_=sa.String(),
            nullable=False,
        )
        batch_op.alter_column('description',
            existing_type=sa.TEXT(),
            type_=sa.String(),
            existing_nullable=True,
        )
        batch_op.alter_column('average_cost',
            existing_type=sa.REAL(),
            server_default=None,
            type_=sa.Float(),
            existing_nullable=True,
        )
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_warehouses_id', 'warehouses', ['warehouse_id'], ['id'])
        batch_op.create_foreign_key('fk_uoms_id', 'uoms', ['default_uom_id'], ['id'])
    op.create_index(op.f('ix_items_item_id'), 'items', ['item_id'], unique=True)
    op.create_index(op.f('ix_items_name'), 'items', ['name'], unique=True)

    # production_operations
    with op.batch_alter_table('production_operations') as batch_op:
        batch_op.alter_column('order_id',
            existing_type=sa.INTEGER(),
            nullable=False,
        )
        batch_op.alter_column('name',
            existing_type=sa.VARCHAR(),
            nullable=False,
        )
    op.create_index(op.f('ix_production_operations_id'), 'production_operations', ['id'], unique=False)

    # production_orders
    with op.batch_alter_table('production_orders') as batch_op:
        batch_op.alter_column('item_id',
            existing_type=sa.INTEGER(),
            nullable=False,
        )
        batch_op.alter_column('start_date',
            existing_type=sa.TIMESTAMP(),
            type_=sa.DateTime(),
            existing_nullable=True,
        )
        batch_op.alter_column('end_date',
            existing_type=sa.TIMESTAMP(),
            type_=sa.DateTime(),
            existing_nullable=True,
        )
    op.create_index(op.f('ix_production_orders_id'), 'production_orders', ['id'], unique=False)

    # purchase_order_lines
    with op.batch_alter_table('purchase_order_lines') as batch_op:
        batch_op.add_column(sa.Column('warehouse_id', sa.Integer(), nullable=True))
        batch_op.alter_column('quantity',
            existing_type=sa.FLOAT(),
            nullable=False,
        )
        batch_op.alter_column('unit_cost',
            existing_type=sa.NUMERIC(precision=12, scale=2),
            type_=sa.Float(),
            nullable=False,
        )
        batch_op.create_foreign_key(
            'fk_purchase_order_lines_warehouses_id',
            'warehouses',
            ['warehouse_id'],
            ['id']
        )
    op.create_index(op.f('ix_purchase_order_lines_id'), 'purchase_order_lines', ['id'], unique=False)

    # transactions
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.alter_column('unit_cost',
            existing_type=sa.NUMERIC(precision=12, scale=2),
            type_=sa.Float(),
            existing_nullable=True,
        )
        batch_op.alter_column('timestamp',
            existing_type=sa.TIMESTAMP(),
            server_default=None,
            type_=sa.DateTime(),
            existing_nullable=True,
        )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)

    # uom_conversions
    with op.batch_alter_table('uom_conversions') as batch_op:
        batch_op.alter_column('item_id',
            existing_type=sa.TEXT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
    op.create_index(op.f('ix_uom_conversions_id'), 'uom_conversions', ['id'], unique=False)

    # work_in_progress
    with op.batch_alter_table('work_in_progress') as batch_op:
        batch_op.alter_column('item_id',
            existing_type=sa.INTEGER(),
            nullable=False,
        )
        batch_op.alter_column('cost_per_unit',
            existing_type=sa.NUMERIC(precision=12, scale=2),
            type_=sa.Float(),
            nullable=False,
        )
        batch_op.alter_column('total_cost',
            existing_type=sa.FLOAT(),
            nullable=False,
        )
        batch_op.alter_column('status',
            existing_type=sa.FLOAT(),
            type_=sa.String(),
            existing_nullable=True,
        )
    op.create_index(op.f('ix_work_in_progress_id'), 'work_in_progress', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema (batch mode)."""

    # Reverse order of upgrade

    op.drop_index(op.f('ix_work_in_progress_id'), table_name='work_in_progress')
    with op.batch_alter_table('work_in_progress') as batch_op:
        batch_op.alter_column('status',
            existing_type=sa.String(),
            type_=sa.FLOAT(),
            existing_nullable=True,
        )
        batch_op.alter_column('total_cost',
            existing_type=sa.FLOAT(),
            nullable=True,
        )
        batch_op.alter_column('cost_per_unit',
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=12, scale=2),
            nullable=True,
        )
        batch_op.alter_column('item_id',
            existing_type=sa.INTEGER(),
            nullable=True,
        )

    op.drop_index(op.f('ix_uom_conversions_id'), table_name='uom_conversions')
    with op.batch_alter_table('uom_conversions') as batch_op:
        batch_op.alter_column('item_id',
            existing_type=sa.Integer(),
            type_=sa.TEXT(),
            existing_nullable=True,
        )

    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.alter_column('timestamp',
            existing_type=sa.DateTime(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            type_=sa.TIMESTAMP(),
            existing_nullable=True,
        )
        batch_op.alter_column('unit_cost',
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=12, scale=2),
            existing_nullable=True,
        )

    with op.batch_alter_table('purchase_order_lines') as batch_op:
        batch_op.drop_constraint('fk_purchase_order_lines_warehouses_id', type_='foreignkey')
        batch_op.drop_column('warehouse_id')
        batch_op.alter_column('unit_cost',
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=12, scale=2),
            nullable=True,
        )
        batch_op.alter_column('quantity',
            existing_type=sa.FLOAT(),
            nullable=True,
        )
    op.drop_index(op.f('ix_purchase_order_lines_id'), table_name='purchase_order_lines')

    op.drop_index(op.f('ix_production_orders_id'), table_name='production_orders')
    with op.batch_alter_table('production_orders') as batch_op:
        batch_op.alter_column('end_date',
            existing_type=sa.DateTime(),
            type_=sa.TIMESTAMP(),
            existing_nullable=True,
        )
        batch_op.alter_column('start_date',
            existing_type=sa.DateTime(),
            type_=sa.TIMESTAMP(),
            existing_nullable=True,
        )
        batch_op.alter_column('item_id',
            existing_type=sa.INTEGER(),
            nullable=True,
        )

    op.drop_index(op.f('ix_production_operations_id'), table_name='production_operations')
    with op.batch_alter_table('production_operations') as batch_op:
        batch_op.alter_column('name',
            existing_type=sa.VARCHAR(),
            nullable=True,
        )
        batch_op.alter_column('order_id',
            existing_type=sa.INTEGER(),
            nullable=True,
        )

    op.drop_index(op.f('ix_items_name'), table_name='items')
    op.drop_index(op.f('ix_items_item_id'), table_name='items')
    with op.batch_alter_table('items') as batch_op:
        batch_op.drop_constraint('fk_uoms_id', type_='foreignkey')
        batch_op.drop_constraint('fk_warehouses_id', type_='foreignkey')
        batch_op.alter_column('average_cost',
            existing_type=sa.Float(),
            server_default=sa.text('(0.0)'),
            type_=sa.REAL(),
            existing_nullable=True,
        )
        batch_op.alter_column('description',
            existing_type=sa.String(),
            type_=sa.TEXT(),
            existing_nullable=True,
        )
        batch_op.alter_column('item_id',
            existing_type=sa.String(),
            type_=sa.TEXT(),
            nullable=True,
        )
        batch_op.alter_column('name',
            existing_type=sa.String(),
            type_=sa.TEXT(),
            existing_nullable=True,
        )
        # re-add old constraints (with ondelete=SET NULL)
        batch_op.create_foreign_key(None, 'uoms', ['default_uom_id'], ['id'], ondelete='SET NULL')
        batch_op.create_foreign_key(None, 'warehouses', ['warehouse_id'], ['id'], ondelete='SET NULL')

    op.drop_index(op.f('ix_inventory_transactions_id'), table_name='inventory_transactions')
    with op.batch_alter_table('inventory_transactions') as batch_op:
        batch_op.alter_column('unit_cost',
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=12, scale=2),
            existing_nullable=True,
        )

    op.drop_index(op.f('ix_inventory_logs_id'), table_name='inventory_logs')
    with op.batch_alter_table('inventory_logs') as batch_op:
        batch_op.drop_constraint('fk_inventory_logs_transaction_id', type_='foreignkey')
        batch_op.alter_column('timestamp',
            existing_type=sa.DateTime(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            type_=sa.TIMESTAMP(),
            existing_nullable=True,
        )
        batch_op.alter_column('transaction_id',
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=True,
        )

    op.drop_index(op.f('ix_boms_id'), table_name='boms')
    with op.batch_alter_table('boms') as batch_op:
        batch_op.alter_column('quantity',
            existing_type=sa.Integer(),
            type_=sa.FLOAT(),
            existing_nullable=True,
        )
