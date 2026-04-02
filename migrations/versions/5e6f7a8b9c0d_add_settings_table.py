"""add settings table

Revision ID: 5e6f7a8b9c0d
Revises: 4d5e6f7a8b9c
Create Date: 2026-04-02

"""
from alembic import op
import sqlalchemy as sa

revision = '5e6f7a8b9c0d'
down_revision = '4d5e6f7a8b9c'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    tables = {row[0] for row in conn.execute(sa.text("SELECT name FROM sqlite_master WHERE type='table'"))}
    if 'settings' not in tables:
        conn.execute(sa.text(
            "CREATE TABLE settings (id INTEGER PRIMARY KEY, family_size REAL NOT NULL DEFAULT 1.0)"
        ))
        conn.execute(sa.text("INSERT INTO settings (id, family_size) VALUES (1, 1.0)"))


def downgrade():
    pass
