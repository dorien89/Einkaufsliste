from app import db

class WeekPlan(db.Model):
    __tablename__ = 'week_plan'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_start = db.Column(db.Date, nullable=False)
    day_index  = db.Column(db.Integer, nullable=False)   # 0=Mo … 6=So
    slot_index = db.Column(db.Integer, nullable=False)   # 0=Frühstück … 4=Abendessen
    recipe_id  = db.Column(db.Integer,
                     db.ForeignKey('recipes.id', ondelete='SET NULL'),
                     nullable=True)

    servings   = db.Column(db.Float, nullable=False, default=1.0)
    is_bought  = db.Column(db.Boolean, nullable=False, default=False)

    recipe = db.relationship('Recipe',
                 backref=db.backref('week_plans', passive_deletes=True))

