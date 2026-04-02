"""add shop_category to manual_shopping_items

Revision ID: 9c0d1e2f3a4b
Revises: 8b9c0d1e2f3a
Create Date: 2026-04-02 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '9c0d1e2f3a4b'
down_revision = '8b9c0d1e2f3a'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    existing = {row[1] for row in conn.execute(sa.text("PRAGMA table_info(manual_shopping_items)"))}
    if 'shop_category' not in existing:
        conn.execute(sa.text(
            "ALTER TABLE manual_shopping_items ADD COLUMN shop_category VARCHAR(100) NOT NULL DEFAULT 'Sonstiges'"
        ))


def downgrade():
    pass  # SQLite cannot drop columns
