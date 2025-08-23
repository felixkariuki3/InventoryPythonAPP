"""Purchase order status update

Revision ID: 4b7fabd946d9
Revises: 9543e52d95e5
Create Date: 2025-08-20 19:31:34.670046
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4b7fabd946d9'
down_revision: Union[str, Sequence[str], None] = '9543e52d95e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with batch alters."""

    # boms
    with op.batch_alter_table("boms") as batch_op:
        batch_op.alter_column("quantity",
            existing_type=sa.FLOAT(),
            type_=sa.Integer(),
            existing_nullable=True
        )
        batch_op.create_index("ix_boms_id", ["id"])

    # inventory_logs
    with op.batch_alter_table("inventory_logs") as batch_op:
        batch_op.alter_column("transaction_id", type_=sa.Integer(), existing_nullable=True)
        batch_op.alter_column("timestamp", type_=sa.DateTime(), existing_nullable=True)
        batch_op.create_index("ix_inventory_logs_id", ["id"])
        batch_op.create_foreign_key("fk_inventory_logs_transaction_id", "transactions", ["transaction_id"], ["id"])

    # inventory_transactions
    with op.batch_alter_table("inventory_transactions") as batch_op:
        batch_op.alter_column("unit_cost", type_=sa.Float(), existing_nullable=True)
        batch_op.create_index("ix_inventory_transactions_id", ["id"])

    # items
    with op.batch_alter_table("items") as batch_op:
        batch_op.alter_column("name", type_=sa.String(), existing_nullable=True)
        batch_op.alter_column("item_id", type_=sa.String(), nullable=False)
        batch_op.alter_column("description", type_=sa.String(), existing_nullable=True)
        batch_op.alter_column("average_cost", type_=sa.Float(), existing_nullable=True)
        batch_op.create_index("ix_items_item_id", ["item_id"], unique=True)
        batch_op.create_index("ix_items_name", ["name"], unique=True)
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key("fk_warehouses_id", "warehouses", ["warehouse_id"], ["id"])
        batch_op.create_foreign_key("fk_uoms_id", "uoms", ["default_uom_id"], ["id"])

    # production_operations
    with op.batch_alter_table("production_operations") as batch_op:
        batch_op.alter_column("order_id", nullable=False)
        batch_op.alter_column("name", nullable=False)
        batch_op.create_index("ix_production_operations_id", ["id"])

    # production_orders
    with op.batch_alter_table("production_orders") as batch_op:
        batch_op.alter_column("item_id", nullable=False)
        batch_op.alter_column("start_date", type_=sa.DateTime(), existing_nullable=True)
        batch_op.alter_column("end_date", type_=sa.DateTime(), existing_nullable=True)
        batch_op.create_index("ix_production_orders_id", ["id"])

        # ✅ add status column for purchase order tracking
        batch_op.add_column(sa.Column("status", sa.String(), nullable=False, server_default="open"))

    # purchase_order_lines
    with op.batch_alter_table("purchase_order_lines") as batch_op:
        batch_op.add_column(sa.Column("received_qty", sa.Float(), nullable=True))
        batch_op.alter_column("quantity", nullable=False)
        batch_op.alter_column("unit_cost", type_=sa.Float(), nullable=False)
        batch_op.create_index("ix_purchase_order_lines_id", ["id"])

    # transactions
    with op.batch_alter_table("transactions") as batch_op:
        batch_op.alter_column("unit_cost", type_=sa.Float(), existing_nullable=True)
        batch_op.alter_column("timestamp", type_=sa.DateTime(), existing_nullable=True)
        batch_op.create_index("ix_transactions_id", ["id"])

    # uom_conversions
    with op.batch_alter_table("uom_conversions") as batch_op:
        batch_op.alter_column("item_id", type_=sa.Integer(), existing_nullable=True)
        batch_op.create_index("ix_uom_conversions_id", ["id"])

    # work_in_progress
    with op.batch_alter_table("work_in_progress") as batch_op:
        batch_op.alter_column("item_id", nullable=False)
        batch_op.alter_column("cost_per_unit", type_=sa.Float(), nullable=False)
        batch_op.alter_column("total_cost", type_=sa.Float(), nullable=False)
        batch_op.alter_column("status", type_=sa.String(), existing_nullable=True)
        batch_op.create_index("ix_work_in_progress_id", ["id"])


def downgrade() -> None:
    """Safe downgrade not fully implemented for batch alters."""
    # For SQLite, full downgrade would need table recreation.
    raise NotImplementedError("Downgrade not implemented. Use backup + downgrade manually if needed.")
