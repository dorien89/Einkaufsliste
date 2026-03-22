"""add is_bought to week_plan

Revision ID: e2f3a4b5c6d7
Revises: d1e2f3a4b5c6
Create Date: 2026-03-22 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'e2f3a4b5c6d7'
down_revision = 'd1e2f3a4b5c6'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('week_plan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_bought', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    with op.batch_alter_table('week_plan', schema=None) as batch_op:
        batch_op.drop_column('is_bought')
