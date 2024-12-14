from app import db


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'Dashboard<{self.id}>'