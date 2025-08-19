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
    # SQLite requires batch mode for altering constraints

    with op.batch_alter_table("purchase_order_lines") as batch_op:
        batch_op.drop_constraint("fk_purchase_order_lines_item_id", type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_purchase_order_lines_item_id",
            "items",
            ["item_id"],
            ["item_id"],
        )


def downgrade():
    with op.batch_alter_table("purchase_order_lines") as batch_op:
        batch_op.drop_constraint("fk_purchase_order_lines_item_id", type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_purchase_order_lines_item_id",
            "items",
            ["item_id"],
            ["id"],  # restoring old FK if downgrading
        )
