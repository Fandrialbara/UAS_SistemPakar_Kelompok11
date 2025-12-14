import pandas as pd

# Load dataset
df = pd.read_csv("model/dataset_penyakit_tanaman.csv")

# Define features
feature_cols = ["Warna_Daun", "Bercak_Daun", "Daun_Layu", "Batang_Busuk", "Pertumbuhan_Terhambat"]

# Input user (sesuai screenshot)
user_input = {
    "Warna_Daun": "Coklat",
    "Bercak_Daun": "Ya",
    "Daun_Layu": "Tidak",
    "Batang_Busuk": "Tidak",
    "Pertumbuhan_Terhambat": "Tidak"
}

print("=" * 80)
print("DEBUG: PENGECEKAN SKOR UNTUK INPUT USER")
print("=" * 80)
print(f"\nInput User:")
for k, v in user_input.items():
    print(f"  {k}: {v}")

# Hitung match dengan setiap baris
results = []
for idx, row in df.iterrows():
    score = 0
    total_input = 0
    
    details = []
    for f in feature_cols:
        if user_input.get(f, "") == "":
            continue
        
        total_input += 1
        user_val = user_input[f].lower()
        row_val = str(row[f]).lower()
        match = "✓" if user_val == row_val else "✗"
        
        if user_val == row_val:
            score += 1
        
        details.append(f"{f}: {user_val} vs {row_val} {match}")
    
    similarity = (score / total_input) * 100 if total_input > 0 else 0
    results.append((row["Penyakit"], row["Nama_Tanaman"], similarity, score, total_input, idx+1))
    
    # Print hanya yang score 100% atau > 50%
    if similarity >= 50:
        print(f"\nBaris {idx+1}: {row['Nama_Tanaman']} → {row['Penyakit']}")
        print(f"  Score: {score}/{total_input} = {similarity:.2f}%")
        for detail in details:
            print(f"    {detail}")

# Kelompokkan berdasarkan penyakit
disease_scores = {}
for disease, plant, score, _, _, _ in results:
    if disease not in disease_scores or score > disease_scores[disease]:
        disease_scores[disease] = (score, plant)

print("\n" + "=" * 80)
print("RANKING PENYAKIT (TERTINGGI KE TERENDAH)")
print("=" * 80)

sorted_results = sorted(disease_scores.items(), key=lambda x: x[1][0], reverse=True)
for i, (disease, (score, plant)) in enumerate(sorted_results[:10], 1):
    print(f"{i}. {disease}: {score:.2f}% (dari {plant})")

print("\n" + "=" * 80)
print(f"HASIL AKHIR: {sorted_results[0][0]} dengan {sorted_results[0][1][0]:.2f}%")
print("=" * 80)
