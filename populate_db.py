import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'einkaufsliste.db')

CATEGORIES = ['Hauptgericht', 'Beilage', 'Vorspeise', 'Dessert', 'Snack']

INGREDIENTS = [
    'Pasta', 'Reis', 'Hähnchenbrust', 'Lachsfilet', 'Knoblauch',
    'Zwiebel', 'Tomaten', 'Paprika', 'Brokkoli', 'Kokosmilch',
    'Currypaste', 'Chili', 'Kreuzkümmel', 'Basilikum', 'Rucola',
    'Butter', 'Olivenöl', 'Salz', 'Pfeffer', 'Parmesan',
    'Schlagsahne', 'Senf', 'Honig', 'Brot', 'Cheddar',
    'Salat', 'Ketchup', 'Mayonnaise', 'Zitronensaft', 'Zucchini',
    'Aubergine', 'Quinoa', 'Avocado', 'Feta', 'Äpfel',
    'Zimt', 'Mehl', 'Eier', 'Nori-Blätter', 'Wasabi',
    'Sojasauce', 'Schokolade', 'Erdbeeren', 'Bananen', 'Marshmallows',
    'Kartoffeln', 'Speck', 'Mozzarella', 'Mascarpone', 'Himbeeren',
    'Löffelbiskuits', 'Kakao', 'Milch', 'Backpulver',
    # New ingredients
    'Hackfleisch', 'Rindfleisch', 'Linsen', 'Tofu', 'Thunfisch',
    'Kichererbsen', 'Bohnen', 'Kürbis', 'Fladenbrot', 'Mango',
    'Joghurt', 'Mais', 'Tortilla', 'Ingwer', 'Champignons',
    'Möhren', 'Sellerie', 'Petersilie', 'Oregano', 'Rosmarin',
    'Paniermehl', 'Rotwein', 'Tomatenmark', 'Zucker', 'Koriander',
    'Lachs', 'Garnelen', 'Spinat', 'Lauch', 'Porree',
    'Sahne', 'Frischkäse', 'Kürbiskerne', 'Walnüsse', 'Mandeln',
    'Haferflocken', 'Vanille', 'Zitrone', 'Orange', 'Weintrauben',
    'Pilze', 'Schinken', 'Thymian', 'Lorbeer', 'Essig',
    'Sesamöl', 'Limette', 'Sojasprossen', 'Frühlingszwiebeln', 'Nudelteig',
]

RECIPES = [
    # ── Hauptgerichte ─────────────────────────────────────────────────────────
    ('Pasta mit Tomatensauce', 'Einfaches Pasta-Gericht mit frischer Tomatensauce.', 'Hauptgericht', [
        ('Pasta', 400, 'g'), ('Tomaten', 500, 'g'), ('Zwiebel', 1, 'Stück'),
        ('Knoblauch', 2, 'Zehen'), ('Olivenöl', 2, 'EL'), ('Basilikum', 10, 'g'),
        ('Parmesan', 40, 'g'), ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Hähnchen Curry mit Reis', 'Aromatisches Curry mit zartem Hähnchen.', 'Hauptgericht', [
        ('Hähnchenbrust', 500, 'g'), ('Reis', 300, 'g'), ('Kokosmilch', 400, 'ml'),
        ('Currypaste', 2, 'EL'), ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'),
        ('Ingwer', 1, 'TL'), ('Salz', 1, 'Prise'),
    ]),
    ('Tomaten-Risotto', 'Cremiges Risotto mit frischen Tomaten und Parmesan.', 'Hauptgericht', [
        ('Reis', 300, 'g'), ('Tomaten', 400, 'g'), ('Zwiebel', 1, 'Stück'),
        ('Knoblauch', 2, 'Zehen'), ('Parmesan', 60, 'g'), ('Butter', 30, 'g'),
        ('Olivenöl', 2, 'EL'), ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Pasta Carbonara', 'Klassisches Nudelgericht mit Ei, Speck und Parmesan.', 'Hauptgericht', [
        ('Pasta', 400, 'g'), ('Speck', 150, 'g'), ('Eier', 3, 'Stück'),
        ('Parmesan', 80, 'g'), ('Knoblauch', 1, 'Zehe'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Spaghetti Bolognese', 'Klassische Bolognese mit Hackfleisch und Tomaten.', 'Hauptgericht', [
        ('Pasta', 400, 'g'), ('Hackfleisch', 500, 'g'), ('Tomaten', 400, 'g'),
        ('Tomatenmark', 2, 'EL'), ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'),
        ('Möhren', 1, 'Stück'), ('Sellerie', 1, 'Stange'), ('Rotwein', 100, 'ml'),
        ('Oregano', 1, 'TL'), ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Vegetarische Lasagne', 'Lasagne mit Zucchini, Auberginen und Béchamelsauce.', 'Hauptgericht', [
        ('Nudelteig', 250, 'g'), ('Zucchini', 250, 'g'), ('Aubergine', 250, 'g'),
        ('Tomaten', 400, 'g'), ('Zwiebel', 1, 'Stück'), ('Schlagsahne', 200, 'ml'),
        ('Parmesan', 60, 'g'), ('Butter', 30, 'g'), ('Mehl', 40, 'g'),
        ('Milch', 500, 'ml'), ('Salz', 1, 'Prise'),
    ]),
    ('Hähnchen-Schnitzel', 'Knusprig paniertes Hähnchenschnitzel.', 'Hauptgericht', [
        ('Hähnchenbrust', 600, 'g'), ('Eier', 2, 'Stück'), ('Paniermehl', 150, 'g'),
        ('Mehl', 80, 'g'), ('Butter', 50, 'g'), ('Zitrone', 1, 'Stück'),
        ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Rindergulasch', 'Würziges Gulasch mit zartem Rindfleisch.', 'Hauptgericht', [
        ('Rindfleisch', 600, 'g'), ('Zwiebel', 3, 'Stück'), ('Paprika', 2, 'Stück'),
        ('Tomatenmark', 2, 'EL'), ('Rotwein', 200, 'ml'), ('Lorbeer', 2, 'Blatt'),
        ('Thymian', 1, 'TL'), ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
        ('Olivenöl', 2, 'EL'),
    ]),
    ('Gemüse-Curry', 'Buntes Gemüsecurry mit Kokosmilch.', 'Hauptgericht', [
        ('Kartoffeln', 400, 'g'), ('Brokkoli', 300, 'g'), ('Paprika', 2, 'Stück'),
        ('Kokosmilch', 400, 'ml'), ('Currypaste', 2, 'EL'), ('Zwiebel', 1, 'Stück'),
        ('Knoblauch', 2, 'Zehen'), ('Ingwer', 1, 'TL'), ('Reis', 300, 'g'),
    ]),
    ('Honig-Senf-Lachs mit Rucola-Nudeln', 'Nudeln mit Honig-Senf-Sauce und Lachs.', 'Hauptgericht', [
        ('Pasta', 400, 'g'), ('Lachsfilet', 400, 'g'), ('Senf', 2, 'EL'),
        ('Honig', 2, 'EL'), ('Rucola', 50, 'g'), ('Olivenöl', 2, 'EL'),
        ('Zitronensaft', 1, 'EL'), ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Gemüse-Quiche', 'Herzhafte Quiche mit Paprika und Käse.', 'Hauptgericht', [
        ('Mehl', 250, 'g'), ('Butter', 125, 'g'), ('Eier', 4, 'Stück'),
        ('Schlagsahne', 200, 'ml'), ('Zwiebel', 2, 'Stück'), ('Paprika', 2, 'Stück'),
        ('Parmesan', 60, 'g'), ('Salz', 1, 'Prise'),
    ]),
    ('Hähnchen-Tikka-Masala', 'Indisches Hähnchen in würziger Tomatensauce.', 'Hauptgericht', [
        ('Hähnchenbrust', 600, 'g'), ('Tomaten', 400, 'g'), ('Joghurt', 150, 'ml'),
        ('Zwiebel', 2, 'Stück'), ('Knoblauch', 3, 'Zehen'), ('Ingwer', 2, 'TL'),
        ('Currypaste', 3, 'EL'), ('Kokosmilch', 200, 'ml'), ('Reis', 300, 'g'),
        ('Koriander', 10, 'g'),
    ]),
    ('Shakshuka', 'Eier in würziger Tomatensauce.', 'Hauptgericht', [
        ('Eier', 4, 'Stück'), ('Tomaten', 500, 'g'), ('Paprika', 2, 'Stück'),
        ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'), ('Chili', 1, 'Stück'),
        ('Kreuzkümmel', 1, 'TL'), ('Olivenöl', 2, 'EL'), ('Feta', 80, 'g'),
        ('Petersilie', 10, 'g'),
    ]),
    ('Ratatouille', 'Provenzalisches Gemüsegericht aus dem Ofen.', 'Hauptgericht', [
        ('Aubergine', 300, 'g'), ('Zucchini', 300, 'g'), ('Tomaten', 400, 'g'),
        ('Paprika', 2, 'Stück'), ('Zwiebel', 2, 'Stück'), ('Knoblauch', 3, 'Zehen'),
        ('Olivenöl', 4, 'EL'), ('Thymian', 1, 'TL'), ('Rosmarin', 1, 'TL'),
        ('Salz', 1, 'Prise'),
    ]),
    ('Pad Thai', 'Gebratene Reisnudeln mit Garnelen und Erdnüssen.', 'Hauptgericht', [
        ('Pasta', 300, 'g'), ('Garnelen', 300, 'g'), ('Eier', 2, 'Stück'),
        ('Sojasprossen', 100, 'g'), ('Frühlingszwiebeln', 3, 'Stück'),
        ('Sojasauce', 3, 'EL'), ('Limette', 1, 'Stück'), ('Sesamöl', 1, 'EL'),
        ('Erdnüsse', 50, 'g'), ('Chili', 1, 'Prise'),
    ]),
    ('Gefüllte Paprika', 'Paprika gefüllt mit Hackfleisch und Reis.', 'Hauptgericht', [
        ('Paprika', 4, 'Stück'), ('Hackfleisch', 400, 'g'), ('Reis', 150, 'g'),
        ('Tomaten', 300, 'g'), ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'),
        ('Oregano', 1, 'TL'), ('Parmesan', 40, 'g'), ('Salz', 1, 'Prise'),
    ]),
    ('Thunfisch-Pasta', 'Schnelle Pasta mit Thunfisch und Kapern.', 'Hauptgericht', [
        ('Pasta', 400, 'g'), ('Thunfisch', 2, 'Dose'), ('Tomaten', 300, 'g'),
        ('Knoblauch', 2, 'Zehen'), ('Olivenöl', 3, 'EL'), ('Petersilie', 15, 'g'),
        ('Zitronensaft', 1, 'EL'), ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Tofu-Gemüse-Stir-Fry', 'Gebratener Tofu mit buntem Gemüse und Sojasauce.', 'Hauptgericht', [
        ('Tofu', 400, 'g'), ('Brokkoli', 300, 'g'), ('Paprika', 1, 'Stück'),
        ('Möhren', 2, 'Stück'), ('Sojasauce', 3, 'EL'), ('Sesamöl', 2, 'EL'),
        ('Ingwer', 1, 'TL'), ('Knoblauch', 2, 'Zehen'), ('Reis', 300, 'g'),
    ]),
    ('Linsen-Bolognese', 'Vegetarische Bolognese mit Linsen.', 'Hauptgericht', [
        ('Linsen', 250, 'g'), ('Pasta', 400, 'g'), ('Tomaten', 400, 'g'),
        ('Tomatenmark', 2, 'EL'), ('Möhren', 2, 'Stück'), ('Sellerie', 2, 'Stangen'),
        ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'), ('Rotwein', 100, 'ml'),
        ('Oregano', 1, 'TL'),
    ]),
    ('Hähnchen mit Pilzsoße', 'Zartes Hähnchen in cremiger Pilzsoße.', 'Hauptgericht', [
        ('Hähnchenbrust', 600, 'g'), ('Champignons', 400, 'g'), ('Sahne', 200, 'ml'),
        ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'), ('Butter', 30, 'g'),
        ('Thymian', 1, 'TL'), ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Garnelen-Pasta', 'Pasta mit Garnelen, Knoblauch und Weißwein.', 'Hauptgericht', [
        ('Pasta', 400, 'g'), ('Garnelen', 400, 'g'), ('Knoblauch', 4, 'Zehen'),
        ('Chili', 1, 'Stück'), ('Olivenöl', 3, 'EL'), ('Petersilie', 15, 'g'),
        ('Zitronensaft', 2, 'EL'), ('Butter', 20, 'g'),
    ]),
    ('Lachsfilet mit Brokkoli', 'Gebratener Lachs mit gedünstetem Brokkoli.', 'Hauptgericht', [
        ('Lachsfilet', 600, 'g'), ('Brokkoli', 500, 'g'), ('Zitrone', 1, 'Stück'),
        ('Butter', 30, 'g'), ('Knoblauch', 2, 'Zehen'), ('Salz', 1, 'Prise'),
        ('Pfeffer', 1, 'Prise'), ('Olivenöl', 2, 'EL'),
    ]),
    ('Spinat-Feta-Pie', 'Blätterteig-Pie mit Spinat und Feta.', 'Hauptgericht', [
        ('Spinat', 500, 'g'), ('Feta', 200, 'g'), ('Eier', 3, 'Stück'),
        ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'), ('Nudelteig', 300, 'g'),
        ('Olivenöl', 2, 'EL'), ('Muskat', 1, 'Prise'), ('Salz', 1, 'Prise'),
    ]),
    ('Mexikanische Tacos', 'Tacos mit gewürztem Hackfleisch und Salsa.', 'Hauptgericht', [
        ('Tortilla', 8, 'Stück'), ('Hackfleisch', 400, 'g'), ('Mais', 1, 'Dose'),
        ('Tomaten', 3, 'Stück'), ('Avocado', 1, 'Stück'), ('Zwiebel', 1, 'Stück'),
        ('Chili', 1, 'TL'), ('Kreuzkümmel', 1, 'TL'), ('Koriander', 15, 'g'),
        ('Limette', 1, 'Stück'),
    ]),
    ('Kürbis-Risotto', 'Cremiges Risotto mit geröstetem Kürbis.', 'Hauptgericht', [
        ('Reis', 300, 'g'), ('Kürbis', 500, 'g'), ('Zwiebel', 1, 'Stück'),
        ('Knoblauch', 2, 'Zehen'), ('Parmesan', 60, 'g'), ('Butter', 40, 'g'),
        ('Olivenöl', 2, 'EL'), ('Rosmarin', 1, 'TL'), ('Salz', 1, 'Prise'),
    ]),
    ('Pilz-Pasta', 'Pasta mit gebratenen Pilzen und Knoblauch.', 'Hauptgericht', [
        ('Pasta', 400, 'g'), ('Champignons', 500, 'g'), ('Knoblauch', 3, 'Zehen'),
        ('Butter', 40, 'g'), ('Parmesan', 50, 'g'), ('Petersilie', 15, 'g'),
        ('Schlagsahne', 100, 'ml'), ('Salz', 1, 'Prise'),
    ]),

    # ── Vorspeisen ────────────────────────────────────────────────────────────
    ('Kartoffelsuppe mit Speck', 'Cremige Suppe aus Kartoffeln mit knusprigem Speck.', 'Vorspeise', [
        ('Kartoffeln', 600, 'g'), ('Speck', 100, 'g'), ('Zwiebel', 2, 'Stück'),
        ('Schlagsahne', 200, 'ml'), ('Butter', 30, 'g'), ('Salz', 1, 'Prise'),
        ('Pfeffer', 1, 'Prise'),
    ]),
    ('Caprese-Salat', 'Frischer Salat mit Tomaten, Mozzarella und Basilikum.', 'Vorspeise', [
        ('Tomaten', 400, 'g'), ('Mozzarella', 250, 'g'), ('Basilikum', 20, 'g'),
        ('Olivenöl', 3, 'EL'), ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Tomatensuppe', 'Cremige Tomatensuppe mit Basilikum.', 'Vorspeise', [
        ('Tomaten', 800, 'g'), ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'),
        ('Schlagsahne', 100, 'ml'), ('Olivenöl', 2, 'EL'), ('Basilikum', 15, 'g'),
        ('Zucker', 1, 'TL'), ('Salz', 1, 'Prise'),
    ]),
    ('Kürbissuppe', 'Samtige Kürbissuppe mit Ingwer und Kokosmilch.', 'Vorspeise', [
        ('Kürbis', 800, 'g'), ('Kokosmilch', 200, 'ml'), ('Ingwer', 2, 'TL'),
        ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'), ('Olivenöl', 2, 'EL'),
        ('Kürbiskerne', 30, 'g'), ('Salz', 1, 'Prise'),
    ]),
    ('Bruschetta', 'Geröstetes Brot mit Tomaten und Basilikum.', 'Vorspeise', [
        ('Brot', 4, 'Scheiben'), ('Tomaten', 300, 'g'), ('Knoblauch', 2, 'Zehen'),
        ('Basilikum', 15, 'g'), ('Olivenöl', 3, 'EL'), ('Salz', 1, 'Prise'),
    ]),
    ('Hummus', 'Cremiger Hummus aus Kichererbsen.', 'Vorspeise', [
        ('Kichererbsen', 400, 'g'), ('Zitronensaft', 3, 'EL'), ('Knoblauch', 2, 'Zehen'),
        ('Olivenöl', 3, 'EL'), ('Kreuzkümmel', 1, 'TL'), ('Salz', 1, 'Prise'),
        ('Fladenbrot', 2, 'Stück'),
    ]),
    ('Linsensuppe', 'Herzhafte Suppe mit roten Linsen.', 'Vorspeise', [
        ('Linsen', 300, 'g'), ('Möhren', 2, 'Stück'), ('Sellerie', 2, 'Stangen'),
        ('Zwiebel', 1, 'Stück'), ('Knoblauch', 2, 'Zehen'), ('Tomaten', 200, 'g'),
        ('Kreuzkümmel', 1, 'TL'), ('Olivenöl', 2, 'EL'), ('Zitronensaft', 1, 'EL'),
    ]),
    ('Caesar Salad', 'Klassischer Salat mit Caesar-Dressing und Croutons.', 'Vorspeise', [
        ('Salat', 300, 'g'), ('Parmesan', 60, 'g'), ('Brot', 100, 'g'),
        ('Mayonnaise', 3, 'EL'), ('Senf', 1, 'TL'), ('Knoblauch', 1, 'Zehe'),
        ('Zitronensaft', 2, 'EL'), ('Olivenöl', 2, 'EL'),
    ]),
    ('Gazpacho', 'Kalte spanische Tomatensuppe.', 'Vorspeise', [
        ('Tomaten', 600, 'g'), ('Paprika', 1, 'Stück'), ('Gurke', 1, 'Stück'),
        ('Zwiebel', 1, 'Stück'), ('Knoblauch', 1, 'Zehe'), ('Olivenöl', 3, 'EL'),
        ('Essig', 2, 'EL'), ('Salz', 1, 'Prise'),
    ]),

    # ── Beilagen ─────────────────────────────────────────────────────────────
    ('Quinoa-Salat mit Avocado und Feta', 'Leichter Salat mit Quinoa und Feta.', 'Beilage', [
        ('Quinoa', 200, 'g'), ('Avocado', 1, 'Stück'), ('Feta', 100, 'g'),
        ('Tomaten', 200, 'g'), ('Rucola', 50, 'g'), ('Olivenöl', 2, 'EL'),
        ('Zitronensaft', 2, 'EL'),
    ]),
    ('Kartoffelsalat', 'Klassischer Kartoffelsalat mit Mayonnaise.', 'Beilage', [
        ('Kartoffeln', 800, 'g'), ('Mayonnaise', 4, 'EL'), ('Zwiebel', 1, 'Stück'),
        ('Senf', 1, 'EL'), ('Essig', 2, 'EL'), ('Petersilie', 15, 'g'),
        ('Salz', 1, 'Prise'), ('Pfeffer', 1, 'Prise'),
    ]),
    ('Couscous-Salat', 'Leichter Couscous-Salat mit Gemüse.', 'Beilage', [
        ('Quinoa', 200, 'g'), ('Paprika', 1, 'Stück'), ('Tomaten', 200, 'g'),
        ('Möhren', 1, 'Stück'), ('Petersilie', 20, 'g'), ('Olivenöl', 3, 'EL'),
        ('Zitronensaft', 2, 'EL'), ('Salz', 1, 'Prise'),
    ]),
    ('Geröstetes Gemüse', 'Buntes Ofengemüse mit Kräutern.', 'Beilage', [
        ('Zucchini', 200, 'g'), ('Aubergine', 200, 'g'), ('Paprika', 2, 'Stück'),
        ('Möhren', 2, 'Stück'), ('Olivenöl', 3, 'EL'), ('Rosmarin', 1, 'TL'),
        ('Thymian', 1, 'TL'), ('Knoblauch', 2, 'Zehen'),
    ]),
    ('Knoblauchbrot', 'Knuspriges Brot mit Knoblauchbutter.', 'Beilage', [
        ('Brot', 1, 'Stück'), ('Butter', 80, 'g'), ('Knoblauch', 3, 'Zehen'),
        ('Petersilie', 15, 'g'), ('Salz', 1, 'Prise'),
    ]),
    ('Grüner Salat', 'Einfacher Blattsalat mit Vinaigrette.', 'Beilage', [
        ('Salat', 300, 'g'), ('Tomaten', 2, 'Stück'), ('Olivenöl', 2, 'EL'),
        ('Essig', 1, 'EL'), ('Senf', 1, 'TL'), ('Salz', 1, 'Prise'),
        ('Pfeffer', 1, 'Prise'),
    ]),
    ('Bohnensalat', 'Herzhafter Salat mit weißen Bohnen.', 'Beilage', [
        ('Bohnen', 400, 'g'), ('Tomaten', 200, 'g'), ('Zwiebel', 1, 'Stück'),
        ('Petersilie', 15, 'g'), ('Olivenöl', 3, 'EL'), ('Zitronensaft', 2, 'EL'),
        ('Salz', 1, 'Prise'),
    ]),
    ('Kichererbsen-Salat', 'Würziger Salat mit Kichererbsen und Feta.', 'Beilage', [
        ('Kichererbsen', 400, 'g'), ('Feta', 100, 'g'), ('Tomaten', 200, 'g'),
        ('Rucola', 50, 'g'), ('Olivenöl', 2, 'EL'), ('Zitronensaft', 2, 'EL'),
        ('Kreuzkümmel', 1, 'TL'),
    ]),

    # ── Desserts ─────────────────────────────────────────────────────────────
    ('Pfannkuchen mit Apfel und Zimt', 'Fluffige Pfannkuchen mit karamellisierten Äpfeln.', 'Dessert', [
        ('Mehl', 200, 'g'), ('Eier', 2, 'Stück'), ('Milch', 300, 'ml'),
        ('Butter', 30, 'g'), ('Äpfel', 3, 'Stück'), ('Zimt', 1, 'TL'),
        ('Zucker', 2, 'EL'), ('Backpulver', 1, 'TL'),
    ]),
    ('Schokoladenfondue', 'Geschmolzene Schokolade zum Dippen.', 'Dessert', [
        ('Schokolade', 200, 'g'), ('Schlagsahne', 150, 'ml'), ('Erdbeeren', 200, 'g'),
        ('Bananen', 2, 'Stück'), ('Marshmallows', 100, 'g'),
    ]),
    ('Himbeer-Tiramisu', 'Sommerliches Tiramisu mit frischen Himbeeren.', 'Dessert', [
        ('Mascarpone', 250, 'g'), ('Schlagsahne', 200, 'ml'), ('Himbeeren', 300, 'g'),
        ('Löffelbiskuits', 200, 'g'), ('Kakao', 2, 'EL'), ('Eier', 3, 'Stück'),
        ('Zucker', 60, 'g'),
    ]),
    ('Apfelkuchen', 'Klassischer Apfelkuchen mit Zimtfüllung.', 'Dessert', [
        ('Mehl', 300, 'g'), ('Butter', 150, 'g'), ('Äpfel', 4, 'Stück'),
        ('Zucker', 100, 'g'), ('Eier', 2, 'Stück'), ('Zimt', 2, 'TL'),
        ('Backpulver', 1, 'TL'), ('Milch', 50, 'ml'),
    ]),
    ('Mousse au Chocolat', 'Luftige Schokoladenmousse.', 'Dessert', [
        ('Schokolade', 200, 'g'), ('Eier', 4, 'Stück'), ('Schlagsahne', 200, 'ml'),
        ('Zucker', 40, 'g'), ('Butter', 30, 'g'),
    ]),
    ('Panna Cotta', 'Cremige Panna Cotta mit Beerensoße.', 'Dessert', [
        ('Schlagsahne', 500, 'ml'), ('Zucker', 60, 'g'), ('Vanille', 1, 'Stück'),
        ('Erdbeeren', 200, 'g'), ('Himbeeren', 100, 'g'), ('Zitronensaft', 1, 'EL'),
    ]),
    ('Waffeln', 'Knusprige Waffeln mit Puderzucker und Früchten.', 'Dessert', [
        ('Mehl', 250, 'g'), ('Eier', 3, 'Stück'), ('Milch', 300, 'ml'),
        ('Butter', 100, 'g'), ('Zucker', 50, 'g'), ('Backpulver', 2, 'TL'),
        ('Erdbeeren', 200, 'g'), ('Vanille', 1, 'TL'),
    ]),
    ('Käsekuchen', 'Cremiger Käsekuchen auf Mürbeteigboden.', 'Dessert', [
        ('Frischkäse', 500, 'g'), ('Zucker', 120, 'g'), ('Eier', 3, 'Stück'),
        ('Mehl', 200, 'g'), ('Butter', 100, 'g'), ('Zitronensaft', 2, 'EL'),
        ('Vanille', 1, 'TL'),
    ]),
    ('Bananenbrot', 'Saftiges Bananenbrot mit Walnüssen.', 'Dessert', [
        ('Bananen', 3, 'Stück'), ('Mehl', 250, 'g'), ('Zucker', 80, 'g'),
        ('Eier', 2, 'Stück'), ('Butter', 80, 'g'), ('Walnüsse', 80, 'g'),
        ('Backpulver', 1, 'TL'), ('Zimt', 1, 'TL'),
    ]),
    ('Mango-Sorbet', 'Erfrischendes Sorbet aus frischer Mango.', 'Dessert', [
        ('Mango', 600, 'g'), ('Zucker', 80, 'g'), ('Limette', 1, 'Stück'),
    ]),

    # ── Snacks ────────────────────────────────────────────────────────────────
    ('Cheeseburger', 'Saftiger Burger mit Cheddar und Beilagen.', 'Snack', [
        ('Hackfleisch', 500, 'g'), ('Brot', 4, 'Stück'), ('Cheddar', 100, 'g'),
        ('Tomaten', 2, 'Stück'), ('Salat', 50, 'g'), ('Mayonnaise', 2, 'EL'),
        ('Senf', 1, 'EL'), ('Ketchup', 2, 'EL'), ('Zwiebel', 1, 'Stück'),
    ]),
    ('Sushi-Platte', 'Auswahl an frischem Maki und Nigiri.', 'Snack', [
        ('Reis', 300, 'g'), ('Lachsfilet', 200, 'g'), ('Nori-Blätter', 5, 'Blatt'),
        ('Wasabi', 1, 'TL'), ('Sojasauce', 50, 'ml'), ('Essig', 2, 'EL'),
    ]),
    ('Avocado Toast', 'Geröstetes Brot mit Avocadocreme.', 'Snack', [
        ('Brot', 2, 'Scheiben'), ('Avocado', 2, 'Stück'), ('Zitronensaft', 1, 'EL'),
        ('Chili', 1, 'Prise'), ('Salz', 1, 'Prise'), ('Eier', 2, 'Stück'),
    ]),
    ('Energie-Bällchen', 'Gesunde Snackbällchen mit Haferflocken.', 'Snack', [
        ('Haferflocken', 200, 'g'), ('Honig', 3, 'EL'), ('Mandeln', 80, 'g'),
        ('Schokolade', 50, 'g'), ('Kokosöl', 2, 'EL'),
    ]),
    ('Nachos mit Salsa', 'Knusprige Nachos mit frischer Tomatensalsa.', 'Snack', [
        ('Tortilla', 200, 'g'), ('Tomaten', 300, 'g'), ('Zwiebel', 1, 'Stück'),
        ('Chili', 1, 'Stück'), ('Koriander', 15, 'g'), ('Limette', 1, 'Stück'),
        ('Cheddar', 100, 'g'),
    ]),
    ('Joghurt mit Früchten und Granola', 'Cremiger Joghurt mit Beeren und Granola.', 'Snack', [
        ('Joghurt', 400, 'g'), ('Erdbeeren', 150, 'g'), ('Himbeeren', 100, 'g'),
        ('Haferflocken', 80, 'g'), ('Honig', 2, 'EL'), ('Mandeln', 30, 'g'),
    ]),
    ('Smoothie Bowl', 'Dicke Smoothie-Bowl mit bunten Toppings.', 'Snack', [
        ('Bananen', 2, 'Stück'), ('Erdbeeren', 200, 'g'), ('Joghurt', 150, 'ml'),
        ('Haferflocken', 50, 'g'), ('Mandeln', 30, 'g'), ('Honig', 1, 'EL'),
        ('Kürbiskerne', 20, 'g'),
    ]),
    ('Wrap mit Hähnchen', 'Gefüllter Wrap mit gegrilltem Hähnchen.', 'Snack', [
        ('Tortilla', 4, 'Stück'), ('Hähnchenbrust', 400, 'g'), ('Salat', 80, 'g'),
        ('Tomaten', 2, 'Stück'), ('Paprika', 1, 'Stück'), ('Mayonnaise', 2, 'EL'),
        ('Senf', 1, 'TL'),
    ]),
]


def populate_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # Categories
        for name in CATEGORIES:
            cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (name,))

        # Ingredients
        for name in INGREDIENTS:
            cursor.execute('INSERT OR IGNORE INTO ingredients (name) VALUES (?)', (name,))

        cursor.execute('SELECT id, name FROM ingredients')
        ingredient_ids = {name: id for id, name in cursor.fetchall()}

        inserted = 0
        skipped = 0
        for name, description, category, ingredients in RECIPES:
            # Skip if recipe already exists
            cursor.execute('SELECT id FROM recipes WHERE name = ?', (name,))
            existing = cursor.fetchone()
            if existing:
                skipped += 1
                continue

            cursor.execute(
                'INSERT INTO recipes (name, description, category) VALUES (?, ?, ?)',
                (name, description, category)
            )
            recipe_id = cursor.lastrowid

            for ing_name, amount, unit in ingredients:
                # Auto-create ingredient if not in list
                if ing_name not in ingredient_ids:
                    cursor.execute('INSERT OR IGNORE INTO ingredients (name) VALUES (?)', (ing_name,))
                    cursor.execute('SELECT id FROM ingredients WHERE name = ?', (ing_name,))
                    ingredient_ids[ing_name] = cursor.fetchone()[0]

                cursor.execute(
                    'INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit) VALUES (?, ?, ?, ?)',
                    (recipe_id, ingredient_ids[ing_name], amount, unit)
                )
            inserted += 1

        connection.commit()
        print(f"Datenbank befüllt: {inserted} Rezepte eingefügt, {skipped} übersprungen (bereits vorhanden).")

    except sqlite3.Error as e:
        print("Fehler:", e)
        connection.rollback()
    finally:
        connection.close()


if __name__ == "__main__":
    populate_database()
