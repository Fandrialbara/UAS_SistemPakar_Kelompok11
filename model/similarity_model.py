import pandas as pd


df = pd.read_csv("model/dataset_penyakit_tanaman.csv")

def diagnose(gejala):
    """
    gejala = dict {
        "Warna_Daun": "Hijau",
        "Bercak_Daun": "Ya",
        "Daun_Layu": "Tidak",
        "Batang_Busuk": "Ya",
        "Pertumbuhan_Terhambat": "Tidak"
    }
    """

    # Jika semua gejala kosong → tidak bisa diagnosis
    if all(v == "" for v in gejala.values()):
        return {
            "penyakit": None,
            "confidence": 0,
            "alasan": "Tidak ada gejala yang diisi"
        }

    scores = []

    for idx, row in df.iterrows():
        cocok = 0
        total = 5 
        
        if gejala["Warna_Daun"] != "" and gejala["Warna_Daun"] == row["Warna_Daun"]:
            cocok += 1
        if gejala["Bercak_Daun"] != "" and gejala["Bercak_Daun"] == row["Bercak_Daun"]:
            cocok += 1
        if gejala["Daun_Layu"] != "" and gejala["Daun_Layu"] == row["Daun_Layu"]:
            cocok += 1
        if gejala["Batang_Busuk"] != "" and gejala["Batang_Busuk"] == row["Batang_Busuk"]:
            cocok += 1
        if gejala["Pertumbuhan_Terhambat"] != "" and gejala["Pertumbuhan_Terhambat"] == row["Pertumbuhan_Terhambat"]:
            cocok += 1

        confidence = (cocok / total) * 100
        if confidence > 0:
            scores.append((row["Penyakit"], confidence, row))

    if not scores:
        return {
            "penyakit": None,
            "confidence": 0,
            "alasan": "Tidak ditemukan kecocokan gejala pada dataset"
        }

    # Ambil penyakit dengan skor tertinggi
    best = max(scores, key=lambda x: x[1])
    penyakit, confidence, row = best

    alasan = (
        f"Penyakit dipilih berdasarkan kecocokan gejala dengan data tanaman {row['Nama_Tanaman']} "
        f"yang memiliki kecocokan {confidence:.2f}%."
    )

    return {
        "penyakit": penyakit,
        "confidence": round(confidence, 2),
        "alasan": alasan
    }