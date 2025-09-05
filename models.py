from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Anggota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False)
    hobi = db.Column(db.String(50), nullable=False)
    moto = db.Column(db.String(50), nullable=False)
    foto = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "alias": self.alias,
            "hobi": self.hobi,
            "moto": self.moto,
            "foto": self.foto,
        }
