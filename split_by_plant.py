import pandas as pd
import os

# Baca dataset
df = pd.read_csv("model/dataset_penyakit_tanaman.csv")

# Buat folder untuk menyimpan file terpisah
output_dir = "model/data_by_plant"
os.makedirs(output_dir, exist_ok=True)

# Dapatkan daftar tanaman unik
plants = df["Nama_Tanaman"].unique()

# Pisahkan data berdasarkan tanaman
for plant in plants:
    plant_data = df[df["Nama_Tanaman"] == plant]
    filename = f"{output_dir}/{plant.replace(' ', '_')}.csv"
    plant_data.to_csv(filename, index=False)
    print(f"✓ {plant}: {len(plant_data)} baris → {filename}")

print(f"\n✓ Total tanaman: {len(plants)}")
print(f"✓ Semua file telah disimpan di folder: {output_dir}")
