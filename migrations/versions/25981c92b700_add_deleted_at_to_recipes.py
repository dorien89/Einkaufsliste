"""add deleted_at to recipes

Revision ID: 25981c92b700
Revises: 2c3d4e5f6a7b
Create Date: 2026-03-30

"""
from alembic import op
import sqlalchemy as sa

revision = '25981c92b700'
down_revision = '2c3d4e5f6a7b'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    existing = {row[1] for row in conn.execute(sa.text("PRAGMA table_info(recipes)"))}
    if 'deleted_at' not in existing:
        conn.execute(sa.text("ALTER TABLE recipes ADD COLUMN deleted_at DATETIME"))


def downgrade():
    pass  # SQLite does not support DROP COLUMN easily; column stays but is ignored
