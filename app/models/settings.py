from app import db


class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    family_size = db.Column(db.Float, nullable=False, default=1.0)

    @classmethod
    def get(cls):
        s = cls.query.get(1)
        if not s:
            s = cls(id=1, family_size=1.0)
            db.session.add(s)
            db.session.commit()
        return s
