"""add week plan table

Revision ID: d1e2f3a4b5c6
Revises: ce3fe4224f99
Create Date: 2026-03-22 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1e2f3a4b5c6'
down_revision = 'ce3fe4224f99'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'week_plan' not in inspector.get_table_names():
        op.create_table(
            'week_plan',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('week_start', sa.Date(), nullable=False),
            sa.Column('day_index', sa.Integer(), nullable=False),
            sa.Column('slot_index', sa.Integer(), nullable=False),
            sa.Column('recipe_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='SET NULL'),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('week_start', 'day_index', 'slot_index', name='uq_week_day_slot')
        )


def downgrade():
    op.drop_table('week_plan')
