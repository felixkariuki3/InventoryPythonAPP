"""Update foreign keys to reference items.item_id instead of items.id"""

from alembic import op


# Revision identifiers
revision = "273a423e8239"
down_revision = "273a423e8199"
branch_labels = None
depends_on = None


def upgrade():
    # BOMs
    op.create_foreign_key(
        "fk_boms_parent_item_id_items", "boms", "items", ["parent_item_id"], ["item_id"]
    )
    op.create_foreign_key(
        "fk_boms_component_item_id_items", "boms", "items", ["component_item_id"], ["item_id"]
    )

    # Inventory Logs
    op.create_foreign_key(
        "fk_inventory_logs_item_id_items", "inventory_logs", "items", ["item_id"], ["item_id"]
    )

    # Inventory Transactions
    op.create_foreign_key(
        "fk_inventory_transactions_item_id_items", "inventory_transactions", "items", ["item_id"], ["item_id"]
    )

    # Production Orders
    op.create_foreign_key(
        "fk_production_orders_item_id_items", "production_orders", "items", ["item_id"], ["item_id"]
    )

    # Purchase Order Lines
    op.create_foreign_key(
        "fk_purchase_order_lines_item_id_items", "purchase_order_lines", "items", ["item_id"], ["item_id"]
    )

    # Transactions
    op.create_foreign_key(
        "fk_transactions_item_id_items", "transactions", "items", ["item_id"], ["item_id"]
    )

    # UOM Conversions
    op.create_foreign_key(
        "fk_uom_conversions_item_id_items", "uom_conversions", "items", ["item_id"], ["item_id"]
    )


def downgrade():
    # Drop them if they exist
    for table, constraint in [
        ("boms", "fk_boms_component_item_id_items"),
        ("inventory_logs", "fk_inventory_logs_item_id_items"),
        ("inventory_transactions", "fk_inventory_transactions_item_id_items"),
        ("production_orders", "fk_production_orders_item_id_items"),
        ("purchase_order_lines", "fk_purchase_order_lines_item_id_items"),
        ("transactions", "fk_transactions_item_id_items"),
        ("uom_conversions", "fk_uom_conversions_item_id_items"),
    ]:
        try:
            op.drop_constraint(constraint, table, type_="foreignkey")
        except Exception:
            pass  # Ignore if missing