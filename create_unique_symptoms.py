import pandas as pd
import os

# Baca dataset
df = pd.read_csv("model/dataset_penyakit_tanaman.csv")

# Kolom gejala (tanpa ID, Nama_Tanaman, Penyakit)
symptom_cols = ['Warna_Daun', 'Bercak_Daun', 'Daun_Layu', 'Batang_Busuk', 'Pertumbuhan_Terhambat']

# Buat kolom kombinasi gejala untuk deteksi duplikat
df['symptom_combo'] = df[symptom_cols].apply(lambda row: '|'.join(row.astype(str)), axis=1)

# Tampilkan informasi duplikat
print("="*70)
print("ANALISIS DUPLIKAT BERDASARKAN KOMBINASI GEJALA")
print("="*70)

duplicate_combos = df[df.duplicated(subset=['symptom_combo'], keep=False)].sort_values('symptom_combo')

if len(duplicate_combos) > 0:
    print(f"\n⚠ Ditemukan {len(duplicate_combos)} baris dengan kombinasi gejala yang sama:\n")
    
    for combo in duplicate_combos['symptom_combo'].unique():
        rows = duplicate_combos[duplicate_combos['symptom_combo'] == combo]
        print(f"Kombinasi: {combo}")
        for idx, row in rows.iterrows():
            print(f"  - {row['Nama_Tanaman']}: {row['Penyakit']}")
        print()
else:
    print("\n✓ Semua kombinasi gejala sudah UNIK!")

# Buat dataset bersih - ambil satu baris per kombinasi gejala
print("="*70)
print("MEMBUAT DATASET DENGAN KOMBINASI GEJALA UNIK")
print("="*70)

df_unique_combo = df.drop_duplicates(subset=['symptom_combo'], keep='first')
df_unique_combo = df_unique_combo.drop('symptom_combo', axis=1)

print(f"\nData sebelum: {len(df)} baris")
print(f"Data setelah: {len(df_unique_combo)} baris")
print(f"Duplikat dihapus: {len(df) - len(df_unique_combo)} baris\n")

# Simpan dataset unik
df_unique_combo.to_csv("model/dataset_penyakit_tanaman_unique_symptoms.csv", index=False)
print("✓ Dataset unik disimpan: model/dataset_penyakit_tanaman_unique_symptoms.csv")

# Analisis: berapa banyak gejala unik per penyakit
print("\n" + "="*70)
print("ANALISIS GEJALA PER PENYAKIT")
print("="*70 + "\n")

for disease in sorted(df_unique_combo['Penyakit'].unique()):
    disease_data = df_unique_combo[df_unique_combo['Penyakit'] == disease]
    print(f"{disease}: {len(disease_data)} kombinasi gejala unik")
    
    # Tampilkan kombinasi gejala untuk penyakit ini
    for idx, row in disease_data.iterrows():
        symptoms = [f"{col}={row[col]}" for col in symptom_cols]
        print(f"  • {' | '.join(symptoms)}")
    print()

# Simpan per penyakit dengan gejala unik
output_dir = "model/data_unique_symptoms_by_disease"
os.makedirs(output_dir, exist_ok=True)

for disease in sorted(df_unique_combo['Penyakit'].unique()):
    disease_data = df_unique_combo[df_unique_combo['Penyakit'] == disease]
    filename = f"{output_dir}/{disease.replace(' ', '_')}.csv"
    disease_data.to_csv(filename, index=False)

print(f"\n✓ File per penyakit disimpan di: {output_dir}")
