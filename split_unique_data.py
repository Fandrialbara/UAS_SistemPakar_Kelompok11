import pandas as pd
import os

# Baca dataset
df = pd.read_csv("model/dataset_penyakit_tanaman.csv")

# Hapus duplikat berdasarkan semua kolom kecuali ID
df_unique = df.drop_duplicates(subset=['Nama_Tanaman', 'Warna_Daun', 'Bercak_Daun', 'Daun_Layu', 'Batang_Busuk', 'Pertumbuhan_Terhambat', 'Penyakit'], keep='first')

print(f"Data sebelum: {len(df)} baris")
print(f"Data setelah: {len(df_unique)} baris")
print(f"Duplikat yang dihapus: {len(df) - len(df_unique)} baris\n")

# Simpan dataset yang sudah di-clean
df_unique.to_csv("model/dataset_penyakit_tanaman_clean.csv", index=False)
print("✓ File bersih disimpan: model/dataset_penyakit_tanaman_clean.csv")

# ===== PISAH BERDASARKAN TANAMAN =====
output_dir_plant = "model/data_by_plant_unique"
os.makedirs(output_dir_plant, exist_ok=True)

plants = df_unique["Nama_Tanaman"].unique()
for plant in plants:
    plant_data = df_unique[df_unique["Nama_Tanaman"] == plant]
    filename = f"{output_dir_plant}/{plant.replace(' ', '_')}.csv"
    plant_data.to_csv(filename, index=False)
    print(f"✓ {plant}: {len(plant_data)} baris unik")

# ===== PISAH BERDASARKAN PENYAKIT =====
output_dir_disease = "model/data_by_disease_unique"
os.makedirs(output_dir_disease, exist_ok=True)

diseases = df_unique["Penyakit"].unique()
for disease in diseases:
    disease_data = df_unique[df_unique["Penyakit"] == disease]
    filename = f"{output_dir_disease}/{disease.replace(' ', '_')}.csv"
    disease_data.to_csv(filename, index=False)
    print(f"✓ {disease}: {len(disease_data)} baris unik")

print(f"\n✓ Semua data unik telah disimpan!")
print(f"  - Tanaman: {output_dir_plant}")
print(f"  - Penyakit: {output_dir_disease}")
