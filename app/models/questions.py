from . import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    responses = db.relationship('Response', backref='question', lazy='dynamic')

    def __repr__(self):
        return f'Question: {self.id=},{self.question=}'

    def __str__(self):
        return self.question


class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'Statistic: {self.id=},{self.agree_count=},{self.disagree_count=}'

    def __str__(self):
        return f'{self.question_id} {self.agree_count} {self.disagree_count}'