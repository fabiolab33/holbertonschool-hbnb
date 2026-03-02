from app import db

class SQLAlchemyRepository:
    """Base repository for SQLAlchemy models"""

    def __init__(self, model):
        self.model = model

    def create(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def list(self):
        return self.model.query.all()

    def update(self, obj):
        db.session.commit()
        return obj

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
