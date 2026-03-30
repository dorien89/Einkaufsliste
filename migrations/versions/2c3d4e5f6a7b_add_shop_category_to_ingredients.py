"""add shop_category to ingredients

Revision ID: 2c3d4e5f6a7b
Revises: 1ab58cc70719
Create Date: 2026-03-30

"""
from alembic import op
import sqlalchemy as sa

revision = '2c3d4e5f6a7b'
down_revision = '1ab58cc70719'
branch_labels = None
depends_on = None

CATEGORY_MAP = {
    'Obst & Gemüse': [
        'Aubergine', 'Avocado', 'Bananen', 'Brokkoli', 'Champignons', 'Chili',
        'Erdbeeren', 'Frühlingszwiebeln', 'Gurke', 'Himbeeren', 'Ingwer',
        'Kartoffeln', 'Knoblauch', 'Kürbis', 'Lauch', 'Limette', 'Mango',
        'Möhren', 'Orange', 'Paprika', 'Petersilie', 'Pilze', 'Porree',
        'Rucola', 'Salat', 'Sellerie', 'Sojasprossen', 'Spinat', 'Tomaten',
        'Weintrauben', 'Zitrone', 'Zucchini', 'Zwiebel', 'Äpfel', 'Basilikum',
        'Koriander',
    ],
    'Fleisch & Fisch': [
        'Garnelen', 'Hackfleisch', 'Hähnchenbrust', 'Lachs', 'Lachsfilet',
        'Rindfleisch', 'Schinken', 'Speck', 'Thunfisch',
    ],
    'Milch & Käse': [
        'Butter', 'Cheddar', 'Eier', 'Feta', 'Frischkäse', 'Joghurt',
        'Mascarpone', 'Milch', 'Mozzarella', 'Parmesan', 'Sahne', 'Schlagsahne',
    ],
    'Brot & Backwaren': [
        'Brot', 'Fladenbrot', 'Haferflocken', 'Löffelbiskuits', 'Tortilla',
    ],
    'Konserven & Fertiggerichte': [
        'Bohnen', 'Currypaste', 'Kichererbsen', 'Kokosmilch', 'Mais',
    ],
    'Nudeln, Reis & Hülsenfrüchte': [
        'Linsen', 'Nudeln', 'Nudelteig', 'Pasta', 'Quinoa', 'Reis',
    ],
    'Öle & Gewürze': [
        'Backpulver', 'Essig', 'Honig', 'Kakao', 'Ketchup', 'Kokosöl',
        'Kreuzkümmel', 'Lorbeer', 'Mayonnaise', 'Mehl', 'Muskat', 'Olivenöl',
        'Oregano', 'Paniermehl', 'Pfeffer', 'Rosmarin', 'Salz', 'Senf',
        'Sesamöl', 'Sojasauce', 'Thymian', 'Tomatenmark', 'Vanille', 'Wasabi',
        'Zimt', 'Zitronensaft', 'Zucker',
    ],
    'Getränke': [
        'Rotwein',
    ],
    'Sonstiges': [
        'Erdnüsse', 'Kürbiskerne', 'Mandeln', 'Marshmallows', 'Nori-Blätter',
        'Schokolade', 'Tofu', 'Walnüsse',
    ],
}


def upgrade():
    conn = op.get_bind()
    existing = {row[1] for row in conn.execute(sa.text("PRAGMA table_info(ingredients)"))}
    if 'shop_category' not in existing:
        conn.execute(sa.text(
            "ALTER TABLE ingredients ADD COLUMN shop_category VARCHAR NOT NULL DEFAULT 'Sonstiges'"
        ))
    for category, names in CATEGORY_MAP.items():
        for name in names:
            conn.execute(
                sa.text("UPDATE ingredients SET shop_category = :cat WHERE name = :name"),
                {"cat": category, "name": name}
            )


def downgrade():
    # SQLite does not support DROP COLUMN in older versions; recreate without it
    conn = op.get_bind()
    conn.execute(sa.text(
        "CREATE TABLE ingredients_backup AS SELECT id, name, default_unit, is_staple FROM ingredients"
    ))
    conn.execute(sa.text("DROP TABLE ingredients"))
    conn.execute(sa.text(
        "ALTER TABLE ingredients_backup RENAME TO ingredients"
    ))
