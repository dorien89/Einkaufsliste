"""change week_plan.servings to float for 0.5-step support

Revision ID: 6f7a8b9c0d1e
Revises: 5e6f7a8b9c0d
Create Date: 2026-04-02

"""
from alembic import op
import sqlalchemy as sa

revision = '6f7a8b9c0d1e'
down_revision = '5e6f7a8b9c0d'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    # SQLite doesn't support ALTER COLUMN — recreate table with REAL servings
    conn.execute(sa.text("""
        CREATE TABLE week_plan_new (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            week_start DATE    NOT NULL,
            day_index  INTEGER NOT NULL,
            slot_index INTEGER NOT NULL,
            recipe_id  INTEGER REFERENCES recipes(id) ON DELETE SET NULL,
            servings   REAL    NOT NULL DEFAULT 1.0,
            is_bought  BOOLEAN NOT NULL DEFAULT 0,
            CONSTRAINT uq_week_day_slot UNIQUE (week_start, day_index, slot_index)
        )
    """))
    conn.execute(sa.text("""
        INSERT INTO week_plan_new
        SELECT id, week_start, day_index, slot_index, recipe_id,
               CAST(servings AS REAL), is_bought
        FROM week_plan
    """))
    conn.execute(sa.text("DROP TABLE week_plan"))
    conn.execute(sa.text("ALTER TABLE week_plan_new RENAME TO week_plan"))


def downgrade():
    pass
