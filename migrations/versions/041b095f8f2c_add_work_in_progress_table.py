"""Add work_in_progress table

Revision ID: create_wip_table
Revises: c67765ac6917
Create Date: 2025-08-13 09:23:25.618620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'create_wip_table'
down_revision: Union[str, Sequence[str], None] = 'c67765ac6917'
branch_labels = None
depends_on = None

def upgrade():
    # Check if table already exists (works for SQLite, PostgreSQL, MySQL)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'work_in_progress' not in inspector.get_table_names():
        op.create_table(
            'work_in_progress',
            sa.Column('id', sa.Integer(), primary_key=True, index=True),
            sa.Column('production_order_id', sa.Integer(), sa.ForeignKey('production_orders.id', name="fk_wip_production_order")),
            sa.Column('item_id', sa.Integer(), sa.ForeignKey('items.item_id', name="fk_wip_item")),
            sa.Column('issued_quantity', sa.Float(), nullable=True),
            sa.Column('cost_per_unit', sa.Float(), nullable=False),
            sa.Column('total_cost', sa.Float(), nullable=False),
            sa.Column('completed_quantity', sa.Float(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True)
        )

def downgrade():
    op.drop_table('work_in_progress')