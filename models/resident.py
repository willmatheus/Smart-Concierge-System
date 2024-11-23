from config import db

class Resident(db.Model):
    cpf = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    apartment_number = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f"<Resident {self.name}>"
