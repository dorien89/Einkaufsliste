"""seed staple ingredients

Revision ID: 1ab58cc70719
Revises: ce3fe4224f99
Create Date: 2026-03-30

"""
from alembic import op
import sqlalchemy as sa

revision = '1ab58cc70719'
down_revision = 'f3a4b5c6d7e8'
branch_labels = None
depends_on = None

STAPLES = [
    'Backpulver', 'Basilikum', 'Chili', 'Essig', 'Honig', 'Kakao',
    'Ketchup', 'Knoblauch', 'Kokosöl', 'Koriander', 'Kreuzkümmel',
    'Lorbeer', 'Mayonnaise', 'Mehl', 'Muskat', 'Olivenöl', 'Oregano',
    'Paniermehl', 'Petersilie', 'Pfeffer', 'Rosmarin', 'Salz', 'Senf',
    'Sesamöl', 'Sojasauce', 'Thymian', 'Tomatenmark', 'Vanille', 'Zimt',
    'Zitronensaft', 'Zucker', 'Zwiebel',
]


def upgrade():
    conn = op.get_bind()
    for name in STAPLES:
        conn.execute(
            sa.text("UPDATE ingredients SET is_staple = 1 WHERE name = :name"),
            {"name": name}
        )


def downgrade():
    conn = op.get_bind()
    for name in STAPLES:
        conn.execute(
            sa.text("UPDATE ingredients SET is_staple = 0 WHERE name = :name"),
            {"name": name}
        )
