from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Anggota
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # supaya bisa diakses React (cross-origin)

db.init_app(app)

# bikin folder uploads kalau belum ada
UPLOAD_FOLDER = os.path.join(app.root_path, "static/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

with app.app_context():
    db.create_all()


# Route testing
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Anomali Meleset API is running 🚀"})


# Ambil semua anggota
@app.route("/api/anggota", methods=["GET"])
def get_anggota():
    anggota = Anggota.query.all()
    return jsonify([a.to_json() for a in anggota])


# Tambah Anggota baru
@app.route("/api/anggota", methods=["POST"])
def tambah_anggota():
    foto_url = None
    if "foto" in request.files:
        file = request.files["foto"]
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        foto_url = f"/static/uploads/{filename}"

    anggota_baru = Anggota(
        nama=request.form.get("nama"),
        alias=request.form.get("alias"),
        hobi=request.form.get("hobi"),
        foto=foto_url,
        moto=request.form.get("moto"),
    )
    db.session.add(anggota_baru)
    db.session.commit()
    return jsonify(anggota_baru.to_json()), 201


# Ambil detail Anggota dengan ID
@app.route("/api/anggota/<int:id>", methods=["GET"])
def get_anggota_by_id(id):
    anggota = Anggota.query.get(id)
    if anggota:
        return jsonify(anggota.to_json())
    return jsonify({"error": "Anggota tidak ada"}), 404


# Hapus Anggota
@app.route("/api/anggota/<int:id>", methods=["DELETE"])
def hapus_anggota(id):
    anggota = Anggota.query.get(id)
    if anggota:
        db.session.delete(anggota)
        db.session.commit()
        return jsonify({"message": "Anggota berhasil dihapus"})
    return jsonify({"message": f"Tidak ada anggota dengan id {id}"})


# Edit Anggota
@app.route("/api/anggota/<int:id>", methods=["PUT"])
def edit_anggota(id):
    anggota = Anggota.query.get(id)
    nama_lama = anggota.nama
    if anggota:
        data = request.get_json()

        anggota.nama = data.get("nama", anggota.nama)
        anggota.alias = data.get("alias", anggota.alias)
        anggota.hobi = data.get("hobi", anggota.hobi)
        anggota.moto = data.get("moto", anggota.moto)
        anggota.foto = data.get("foto", anggota.foto)

        db.session.commit()
        return jsonify({"message": f"Anggota {nama_lama} berhasil di update"})
    return jsonify({"error": f"Anggota dengan id {id} tidak ada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
