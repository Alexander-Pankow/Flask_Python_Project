from app.models import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    questions = db.relationship("Question", backref="category", lazy=True)

    def __repr__(self):
        return f"Category({self.name})"