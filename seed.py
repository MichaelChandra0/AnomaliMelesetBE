from app import app
from models import db, Anggota

with app.app_context():
    db.drop_all()  # hapus tabel lama (opsional, biar fresh)
    db.create_all()  # bikin tabel baru

    dummy_anggota = [
        Anggota(
            nama="Dervin",
            alias="DRStore",
            hobi="ngocok",
            foto="https://via.placeholder.com/150",
            moto="Banyak Ngocok itu indah",
        ),
        Anggota(
            nama="Michael",
            alias="Jack",
            hobi="ngoding",
            foto="https://via.placeholder.com/112",
            moto="Banyak ngoding itu indah",
        ),
    ]

    db.session.add_all(dummy_anggota)
    db.session.commit()

    print("✅ Dummy data inserted!")
