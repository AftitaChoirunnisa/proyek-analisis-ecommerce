import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="E-Commerce Public Analytics Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# 2. CSS Kustom untuk Mempercantik Tampilan (Gaya Modern & Clean)
st.markdown("""
    <style>
    /* Mengatur latar belakang utama aplikasi */
    .stApp {
        background-color: #F4F7F6;
    }
    
    /* Styling untuk Kotak Metrik / KPI Cards */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Styling Header */
    h1, h2, h3 {
        color: #1E293B;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# Mengatur tema visualisasi seaborn agar selaras
sns.set_theme(style="whitegrid")

# Fungsi untuk memuat dataset dengan caching
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])
    return df

all_df = load_data()

# ==========================================
# SIDEBAR (FILTER)
# ==========================================
st.sidebar.markdown("## 🔍 Filter Data")
st.sidebar.markdown("Pilih rentang waktu transaksi:")

min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

start_date, end_date = st.sidebar.date_input(
    label="Rentang Tanggal:",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

filtered_df = all_df[
    (all_df["order_purchase_timestamp"].dt.date >= start_date) &
    (all_df["order_purchase_timestamp"].dt.date <= end_date)
]

st.sidebar.markdown("---")
st.sidebar.info("💡 **Info**: Dashboard interaktif untuk analisis E-Commerce Public Dataset.")

# ==========================================
# MAIN PAGE
# ==========================================
st.title("🛍️ E-Commerce Business Dashboard")
st.markdown("Analisis komprehensif performa penjualan, logistik, dan segmentasi pelanggan.")
st.markdown("<br>", unsafe_allow_html=True)

# Baris 1: Key Performance Indicators (KPIs)
st.markdown("### 📊 Ringkasan Performa (KPIs)")
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df["price"].sum()
total_orders = filtered_df["order_id"].nunique()
avg_rating = filtered_df["review_score"].mean()
total_customers = filtered_df["customer_unique_id"].nunique()

with col1:
    st.metric("Total Revenue", f"BRL {total_revenue:,.0f}")
with col2:
    st.metric("Total Orders", f"{total_orders:,}")
with col3:
    st.metric("Average Review Score", f"{avg_rating:.2f} ★")
with col4:
    st.metric("Active Customers", f"{total_customers:,}")

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# PERTANYAAN 1: KATEGORI PRODUK
# ==========================================
st.markdown("### 1. Performa Pendapatan Kategori Produk")

category_rev = filtered_df.groupby("product_category_name_english").agg({
    "price": "sum",
    "order_id": "nunique"
}).rename(columns={"price": "total_revenue", "order_id": "total_orders"}).reset_index()

category_rev = category_rev[category_rev["product_category_name_english"] != "others"]
top_5 = category_rev.sort_values(by="total_revenue", ascending=False).head(5)
bot_5 = category_rev.sort_values(by="total_revenue", ascending=True).head(5)

fig1, ax1 = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

sns.barplot(
    x="total_revenue", y="product_category_name_english",
    data=top_5, hue="product_category_name_english", palette="Blues_r", legend=False, ax=ax1[0]
)
ax1[0].set_title("5 Kategori Produk dengan Revenue Tertinggi", fontsize=13, weight="bold")
ax1[0].set_xlabel("Total Revenue (BRL)")
ax1[0].set_ylabel(None)

for p in ax1[0].patches:
    ax1[0].annotate(
        f"{p.get_width():,.0f} BRL",
        (p.get_width() * 0.70, p.get_y() + p.get_height() / 2.),
        ha="center", va="center", color="white", weight="bold"
    )

sns.barplot(
    x="total_revenue", y="product_category_name_english",
    data=bot_5, hue="product_category_name_english", palette="Reds", legend=False, ax=ax1[1]
)
ax1[1].set_title("5 Kategori Produk dengan Revenue Terendah", fontsize=13, weight="bold")
ax1[1].set_xlabel("Total Revenue (BRL)")
ax1[1].set_ylabel(None)

for p in ax1[1].patches:
    ax1[1].annotate(
        f"{p.get_width():,.2f} BRL",
        (p.get_width() + 20, p.get_y() + p.get_height() / 2.),
        ha="left", va="center", color="black", weight="bold"
    )

st.pyplot(fig1)
st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# PERTANYAAN 2: DAMPAK LOGISTIK
# ==========================================
st.markdown("### 2. Pengaruh Ketepatan Waktu Logistik terhadap Skor Ulasan")

delivery_impact = filtered_df.groupby("delivery_status").agg({
    "review_score": ["mean", "count"]
}).reset_index()
delivery_impact.columns = ["delivery_status", "avg_review_score", "total_orders"]

fig2, ax2 = plt.subplots(figsize=(8, 4.5))
palette_colors = ["#D9534F", "#2E6DA4"]
bars = sns.barplot(
    x="delivery_status", y="avg_review_score",
    data=delivery_impact, hue="delivery_status", palette=palette_colors, legend=False, ax=ax2
)
ax2.set_title("Rata-rata Skor Ulasan: Tepat Waktu vs Terlambat", fontsize=12, weight="bold")
ax2.set_xlabel("Status Pengiriman")
ax2.set_ylabel("Rata-rata Skor Ulasan (1 - 5)")
ax2.set_ylim(0, 5.2)

for i, p in enumerate(bars.patches):
    score = delivery_impact.loc[i, "avg_review_score"]
    tot = delivery_impact.loc[i, "total_orders"]
    bars.annotate(
        f"{score:.2f} ★",
        (p.get_x() + p.get_width() / 2., p.get_height() / 2),
        ha="center", va="center", color="white", weight="bold", fontsize=13
    )
    bars.annotate(
        f"({tot:,} pesanan)",
        (p.get_x() + p.get_width() / 2., p.get_height() + 0.15),
        ha="center", va="bottom", color="dimgray", weight="bold", fontsize=10
    )

st.pyplot(fig2)
st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# RFM ANALYSIS
# ==========================================
st.markdown("### 3. Analisis Lanjutan: Segmentasi Pelanggan (RFM Metrics)")

snapshot_date = filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
rfm_df = filtered_df.groupby("customer_unique_id").agg({
    "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
    "order_id": "nunique",
    "price": "sum"
}).reset_index()
rfm_df.columns = ["customer_unique_id", "recency", "frequency", "monetary"]

fig3, ax3 = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))

top_rec = rfm_df.sort_values(by="recency", ascending=True).head(5)
sns.barplot(y="customer_unique_id", x="recency", data=top_rec, hue="customer_unique_id", palette="crest", legend=False, ax=ax3[0])
ax3[0].set_title("Top 5 by Recency (Days)", weight="bold")
ax3[0].set_xlabel("Hari Terakhir Transaksi")
ax3[0].set_ylabel(None)

top_freq = rfm_df.sort_values(by="frequency", ascending=False).head(5)
sns.barplot(y="customer_unique_id", x="frequency", data=top_freq, hue="customer_unique_id", palette="crest", legend=False, ax=ax3[1])
ax3[1].set_title("Top 5 by Frequency (Orders)", weight="bold")
ax3[1].set_xlabel("Jumlah Order")
ax3[1].set_ylabel(None)

top_mon = rfm_df.sort_values(by="monetary", ascending=False).head(5)
sns.barplot(y="customer_unique_id", x="monetary", data=top_mon, hue="customer_unique_id", palette="crest", legend=False, ax=ax3[2])
ax3[2].set_title("Top 5 by Monetary (Revenue)", weight="bold")
ax3[2].set_xlabel("Total Belanja (BRL)")
ax3[2].set_ylabel(None)

st.pyplot(fig3)