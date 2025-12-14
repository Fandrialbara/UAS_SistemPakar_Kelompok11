Sistem Pakar - Fuzzy-like (otomatis dari dataset)
================================================

Isi folder:
- app.py                 : Flask app
- requirements.txt       : pip dependencies
- templates/             : HTML templates
- static/                : CSS
- model/fuzzy_model.py   : model dan inferensi
- model/dataset_penyakit_tanaman.csv : dataset (dari upload)

Jalankan:
1. python -m venv venv
2. source venv/bin/activate   (Linux/Mac) atau venv\Scripts\activate (Windows)
3. pip install -r requirements.txt
4. python app.py
5. Buka http://127.0.0.1:5000

Catatan:
- Implementasi ini membuat aturan otomatis dari setiap baris dataset.
- Derajat keyakinan adalah rasio kecocokan antar fitur (simple fuzzy-like).
