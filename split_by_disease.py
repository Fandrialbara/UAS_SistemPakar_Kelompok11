import pandas as pd
import os

# Baca dataset
df = pd.read_csv("model/dataset_penyakit_tanaman.csv")

# Buat folder untuk menyimpan file terpisah
output_dir = "model/data_by_disease"
os.makedirs(output_dir, exist_ok=True)

# Dapatkan daftar penyakit unik
diseases = df["Penyakit"].unique()

# Pisahkan data berdasarkan penyakit
for disease in diseases:
    disease_data = df[df["Penyakit"] == disease]
    filename = f"{output_dir}/{disease.replace(' ', '_')}.csv"
    disease_data.to_csv(filename, index=False)
    print(f"✓ {disease}: {len(disease_data)} baris → {filename}")

print(f"\n✓ Total penyakit: {len(diseases)}")
print(f"✓ Semua file telah disimpan di folder: {output_dir}")
