from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# ===============================
# LOAD DATASET
# ===============================
df = pd.read_csv("model/dataset_penyakit_tanaman.csv")


# Pastikan kolom-kolom sesuai dataset (hanya gejala, bukan identitas)
feature_cols = ["Warna_Daun", "Bercak_Daun", "Daun_Layu", "Batang_Busuk", "Pertumbuhan_Terhambat"]

# ===============================
# DESKRIPSI PENYAKIT (ALASAN OUTPUT)
# ===============================
disease_desc = {
    "Busuk Lunak": "Disebabkan oleh bakteri pemicu pelapukan jaringan basah pada tanaman.",
    "Karat Daun": "Infeksi jamur yang membuat daun muncul bintik coklat berkarat.",
    "Busuk Hitam": "Penyebab utama adalah bakteri/jamur yang menyerang akar dan batang.",
    "Hawar Daun Bakteri": "Infeksi bakteri yang menyebabkan bercak dan pengeringan daun.",
    "Antraknosa": "Penyakit jamur yang menyerang daun dan buah dengan bercak kehitaman.",
    "Bercak Daun": "Infeksi jamur/bakteri yang memunculkan bercak pada daun.",
    "Bercak Daun Cercospora": "Bercak daun parah berasal dari jamur Cercospora.",
    "Busuk Akar": "Kerusakan akar menyebabkan tanaman layu dan tidak bisa menyerap air.",
    "Layu Bakteri": "Bakteri pemicu kelayuan total pada daun dan batang.",
    "Embun Tepung": "Jamur berwarna putih menyerupai bedak pada daun.",
    "Busuk Akar Phytophthora": "Jamur Phytophthora menyerang akar hingga membusuk.",
    "Busuk Buah Botrytis": "Jamur Botrytis menyebabkan buah membusuk dan berjamur.",
    "Layu Fusarium": "Penyakit layu kronis yang disebabkan oleh jamur Fusarium.",
    "Jamur Upas": "Jamur parasit yang menyerang batang dan daun.",
    "Busuk Akar": "Kerusakan akar akibat patogen sehingga tanaman tidak menyerap nutrisi."
}

# ===============================
# FUNCTION PEMBANDING GEJALA (IF-THEN)
# ===============================
def calculate_match(user_input, row):
    """Menghitung tingkat kemiripan berdasarkan gejala yang cocok"""
    score = 0
    total_input = 0  # Hitung hanya gejala yang diisi user

    for f in feature_cols:
        if user_input.get(f, "") == "":
            continue  # Skip gejala kosong
        
        total_input += 1  # +1 untuk setiap gejala yang diisi
        
        if user_input[f].lower() == str(row[f]).lower():
            score += 1

    # Hitung similarity berdasarkan gejala yang diisi saja
    similarity = (score / total_input) * 100 if total_input > 0 else 0
    return similarity


# ===============================
# HALAMAN UTAMA
# ===============================
@app.route("/")
def index():
    options = {}

    for col in feature_cols:  # semua gejala
        options[col] = sorted(df[col].astype(str).unique())

    plant_names = sorted(df["Nama_Tanaman"].unique())

    return render_template("index.html", plant_names=plant_names, options=options)


# PROSES DIAGNOSA

@app.route("/diagnose", methods=["POST"])
def diagnose():
    # ambil input user
    user_input = {feature: request.form.get(feature, "").strip() for feature in feature_cols}
    plant_selected = request.form.get("Nama_Tanaman", "").strip()

    # hitung tingkat kecocokan dengan rule IF–THEN
    results = []
    for _, row in df.iterrows():
        match_score = calculate_match(user_input, row)
        results.append((row["Penyakit"], match_score, row["Nama_Tanaman"]))

    # PRIORITAS 1: Jika user pilih tanaman, filter berdasarkan tanaman itu
    if plant_selected:
        results_filtered = [r for r in results if r[2] == plant_selected]
        if results_filtered:
            results = results_filtered

    # PRIORITAS 2: Ambil score tertinggi
    if results:
        top_disease = max(results, key=lambda x: x[1])
        top_result = [(top_disease[0], top_disease[1])]
    else:
        top_result = []

    return render_template(
        "result.html",
        inputs=user_input,
        results=top_result,
        disease_desc=disease_desc
    )

if __name__ == "__main__":
    app.run(debug=True)
