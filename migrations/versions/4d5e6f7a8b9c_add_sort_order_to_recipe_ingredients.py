"""add sort_order to recipe_ingredients

Revision ID: 4d5e6f7a8b9c
Revises: 25981c92b700
Create Date: 2026-04-02

"""
from alembic import op
import sqlalchemy as sa

revision = '4d5e6f7a8b9c'
down_revision = '25981c92b700'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    existing = {row[1] for row in conn.execute(sa.text("PRAGMA table_info(recipe_ingredients)"))}
    if 'sort_order' not in existing:
        conn.execute(sa.text("ALTER TABLE recipe_ingredients ADD COLUMN sort_order INTEGER DEFAULT 0"))


def downgrade():
    pass  # SQLite does not support DROP COLUMN easily; column stays but is ignored
