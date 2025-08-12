"""Add foreign keys to inventory transactions - SQLite safe"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '273a423e8199'
down_revision: Union[str, Sequence[str], None] = '584829e655bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# --- Utility functions ---
def table_exists(table_name: str) -> bool:
    conn = op.get_bind()
    result = conn.execute(
        sa.text("SELECT name FROM sqlite_master WHERE type='table' AND name=:name"),
        {"name": table_name}
    ).fetchone()
    return result is not None

def index_exists(index_name: str) -> bool:
    conn = op.get_bind()
    result = conn.execute(
        sa.text("SELECT name FROM sqlite_master WHERE type='index' AND name=:name"),
        {"name": index_name}
    ).fetchone()
    return result is not None

def safe_drop_constraint(batch_op, name, type_):
    try:
        batch_op.drop_constraint(name, type_=type_)
    except ValueError:
        pass  # Ignore if constraint not found


# --- Upgrade ---
def upgrade() -> None:
    """Upgrade schema safely for SQLite"""

    # Drop index if exists
    if index_exists("ix_work_in_progress_id"):
        with op.batch_alter_table('work_in_progress', schema=None) as batch_op:
            batch_op.drop_index("ix_work_in_progress_id")

    # Drop table if exists
    if table_exists("work_in_progress"):
        op.drop_table("work_in_progress")

    # BOMS table
    if table_exists("boms"):
        with op.batch_alter_table('boms', schema=None) as batch_op:
            safe_drop_constraint(batch_op, 'fk_boms_parent_item_id_items', type_='foreignkey')
            safe_drop_constraint(batch_op, 'fk_boms_component_item_id_items', type_='foreignkey')
            batch_op.create_foreign_key(None, 'items', ['parent_item_id'], ['item_id'])
            batch_op.create_foreign_key(None, 'items', ['component_item_id'], ['item_id'])

    # Inventory logs
    if table_exists("inventory_logs"):
        with op.batch_alter_table('inventory_logs', schema=None) as batch_op:
            safe_drop_constraint(batch_op, 'fk_inventory_logs_item_id_items', type_='foreignkey')
            batch_op.create_foreign_key(None, 'items', ['item_id'], ['item_id'])

    # Inventory transactions
    if table_exists("inventory_transactions"):
        with op.batch_alter_table('inventory_transactions', schema=None) as batch_op:
            safe_drop_constraint(batch_op, 'fk_inventory_transactions_item_id_items', type_='foreignkey')
            batch_op.create_foreign_key(None, 'items', ['item_id'], ['item_id'])

    # Items table
    if table_exists("items"):
        with op.batch_alter_table('items', schema=None) as batch_op:
            batch_op.alter_column('item_id',
                existing_type=sa.INTEGER(),
                type_=sa.String(),
                existing_nullable=True
            )
            if not index_exists("ix_items_item_id"):
                batch_op.create_index("ix_items_item_id", ['item_id'], unique=True)
            safe_drop_constraint(batch_op, 'fk_items_item_id_items', type_='foreignkey')

    # Production operations
    if table_exists("production_operations"):
        with op.batch_alter_table('production_operations', schema=None) as batch_op:
            batch_op.alter_column('order_id', existing_type=sa.INTEGER(), nullable=False)
            batch_op.alter_column('name', existing_type=sa.VARCHAR(), nullable=False)

    # Production orders
    if table_exists("production_orders"):
        with op.batch_alter_table('production_orders', schema=None) as batch_op:
            batch_op.alter_column('item_id', existing_type=sa.INTEGER(), nullable=False)
            safe_drop_constraint(batch_op, 'fk_production_orders_item_id_items', type_='foreignkey')
            batch_op.create_foreign_key(None, 'items', ['item_id'], ['item_id'])

    # Purchase order lines
    if table_exists("purchase_order_lines"):
        with op.batch_alter_table('purchase_order_lines', schema=None) as batch_op:
            safe_drop_constraint(batch_op, 'fk_purchase_order_lines_item_id_items', type_='foreignkey')
            batch_op.create_foreign_key(None, 'items', ['item_id'], ['item_id'])

    # Transactions table
    if table_exists("transactions"):
        with op.batch_alter_table('transactions', schema=None) as batch_op:
            safe_drop_constraint(batch_op, 'fk_transactions_item_id_items', type_='foreignkey')
            batch_op.create_foreign_key(None, 'items', ['item_id'], ['item_id'])

    # UOM conversions
    if table_exists("uom_conversions"):
        with op.batch_alter_table('uom_conversions', schema=None) as batch_op:
            safe_drop_constraint(batch_op, 'fk_uom_conversions_item_id_items', type_='foreignkey')
            batch_op.create_foreign_key(None, 'items', ['item_id'], ['item_id'])


# --- Downgrade ---
def downgrade() -> None:
    """(Optional) You can implement reverse logic here if needed"""
    pass
