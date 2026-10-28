# Dicoding Collection Dashboard ✨
# Proyek Analisis Data: E-Commerce Public Dataset ✨

Dashboard interaktif ini dirancang untuk menganalisis performa pendapatan kategori produk, efisiensi waktu logistik, serta segmentasi pelanggan (RFM Analysis) dari E-Commerce Public Dataset.

## Struktur Direktori
- `dashboard/`: Berisi skrip aplikasi Streamlit (`dashboard.py`) dan dataset bersih (`main_data.csv`).
- `data/`: Kumpulan dataset mentah berformat CSV.
- `notebook.ipynb`: Jupyter Notebook yang berisi seluruh tahapan analisis (Data Wrangling, EDA, Visualization, RFM).
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.

## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
mkdir proyek_analisis_data
cd proyek_analisis_data
pip install -r requirements.txt

## Run steamlit app
streamlit run dashboard/dashboard.py