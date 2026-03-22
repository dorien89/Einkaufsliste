"""add servings to week_plan

Revision ID: f3a4b5c6d7e8
Revises: e2f3a4b5c6d7
Create Date: 2026-03-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'f3a4b5c6d7e8'
down_revision = 'e2f3a4b5c6d7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('week_plan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('servings', sa.Integer(), nullable=False, server_default='1'))


def downgrade():
    with op.batch_alter_table('week_plan', schema=None) as batch_op:
        batch_op.drop_column('servings')
