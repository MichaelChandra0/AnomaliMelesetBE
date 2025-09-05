from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Anggota
import cloudinary
import cloudinary.uploader
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # supaya bisa diakses React (cross-origin)

db.init_app(app)

# setup cloudinary
cloudinary.config(
    cloud_name=app.config["CLOUD_NAME"],
    api_key=app.config["API_KEY"],
    api_secret=app.config["API_SECRET"],
)

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
def create_event():

    foto_url = None
    if "foto" in request.files:
        file = request.files["foto"]
        upload_result = cloudinary.uploader.upload(file)
        foto_url = upload_result["secure_url"]

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
