"""multi-recipe slots and manual shopping items

Revision ID: 8b9c0d1e2f3a
Revises: a795fc92c6e1
Create Date: 2026-04-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '8b9c0d1e2f3a'
down_revision = '6f7a8b9c0d1e'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # 1. Drop uq_week_day_slot from week_plan by recreating the table (SQLite limitation)
    tables = {row[0] for row in conn.execute(sa.text("SELECT name FROM sqlite_master WHERE type='table'"))}

    if 'week_plan' in tables:
        conn.execute(sa.text("""
            CREATE TABLE week_plan_new (
                id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                week_start DATE    NOT NULL,
                day_index  INTEGER NOT NULL,
                slot_index INTEGER NOT NULL,
                recipe_id  INTEGER REFERENCES recipes(id) ON DELETE SET NULL,
                servings   FLOAT   NOT NULL DEFAULT 1.0,
                is_bought  BOOLEAN NOT NULL DEFAULT 0
            )
        """))
        conn.execute(sa.text("INSERT INTO week_plan_new SELECT id, week_start, day_index, slot_index, recipe_id, servings, is_bought FROM week_plan"))
        conn.execute(sa.text("DROP TABLE week_plan"))
        conn.execute(sa.text("ALTER TABLE week_plan_new RENAME TO week_plan"))

    # 2. Create manual_shopping_items table
    if 'manual_shopping_items' not in tables:
        conn.execute(sa.text("""
            CREATE TABLE manual_shopping_items (
                id         INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                name       VARCHAR(200) NOT NULL,
                amount     FLOAT,
                unit       VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))


def downgrade():
    conn = op.get_bind()

    # Re-add the unique constraint (drop duplicates first to avoid constraint violation)
    conn.execute(sa.text("""
        DELETE FROM week_plan WHERE id NOT IN (
            SELECT MIN(id) FROM week_plan GROUP BY week_start, day_index, slot_index
        )
    """))
    conn.execute(sa.text("""
        CREATE TABLE week_plan_old (
            id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            week_start DATE    NOT NULL,
            day_index  INTEGER NOT NULL,
            slot_index INTEGER NOT NULL,
            recipe_id  INTEGER REFERENCES recipes(id) ON DELETE SET NULL,
            servings   FLOAT   NOT NULL DEFAULT 1.0,
            is_bought  BOOLEAN NOT NULL DEFAULT 0,
            UNIQUE (week_start, day_index, slot_index)
        )
    """))
    conn.execute(sa.text("INSERT INTO week_plan_old SELECT * FROM week_plan"))
    conn.execute(sa.text("DROP TABLE week_plan"))
    conn.execute(sa.text("ALTER TABLE week_plan_old RENAME TO week_plan"))

    conn.execute(sa.text("DROP TABLE IF EXISTS manual_shopping_items"))
