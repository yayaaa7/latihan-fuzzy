import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. FUNGSI KEANGGOTAAN FUZZY (MANUAL) ---
def fuzzifikasi_rendah(x):
    if x <= 40:
        return 1.0
    elif 40 < x < 60:
        return (60 - x) / (60 - 40)
    else:
        return 0.0

def fuzzifikasi_sedang(x):
    if x <= 40 or x >= 80:
        return 0.0
    elif 40 < x <= 60:
        return (x - 40) / (60 - 40)
    elif 60 < x < 80:
        return (80 - x) / (80 - 60)

def fuzzifikasi_tinggi(x):
    if x <= 60:
        return 0.0
    elif 60 < x < 80:
        return (x - 60) / (80 - 60)
    else:
        return 1.0

# --- 2. PENGATURAN HALAMAN STREAMLIT ---
st.set_page_config(page_title="Fuzzy Logika - Penilaian Mahasiswa", layout="centered")

st.title("🎓 Aplikasi Logika Fuzzy: Penilaian Mahasiswa")
st.write("Aplikasi ini menghitung derajat keanggotaan nilai ujian mahasiswa ke dalam kategori **Rendah**, **Sedang**, dan **Tinggi**.")

st.markdown("---")

# --- 3. INTERFACE INPUT ---
st.sidebar.header("📥 Input Nilai")
nilai_input = st.sidebar.slider(
    "Masukkan Nilai Ujian Mahasiswa:",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=0.5
)

# Hitung nilai fuzzy berdasarkan input
u_rendah = fuzzifikasi_rendah(nilai_input)
u_sedang = fuzzifikasi_sedang(nilai_input)
u_tinggi = fuzzifikasi_tinggi(nilai_input)

# --- 4. GRAFIK HIMPUNAN FUZZY ---
st.subheader("📊 Grafik Fungsi Keanggotaan")

# Generate data untuk plot kurva
x_vals = np.linspace(0, 100, 500)
y_rendah = [fuzzifikasi_rendah(x) for x in x_vals]
y_sedang = [fuzzifikasi_sedang(x) for x in x_vals]
y_tinggi = [fuzzifikasi_tinggi(x) for x in x_vals]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x_vals, y_rendah, label="Rendah", color="blue", linewidth=2)
ax.plot(x_vals, y_sedang, label="Sedang", color="green", linewidth=2)
ax.plot(x_vals, y_tinggi, label="Tinggi", color="red", linewidth=2)

# Tambahkan garis penanda posisi input user
ax.axvline(x=nilai_input, color="purple", linestyle="--", label=f"Input ({nilai_input})")
ax.scatter([nilai_input]*3, [u_rendah, u_sedang, u_tinggi], color="black", zorder=5)

ax.set_title("Kurva Keanggotaan Nilai Ujian", fontsize=12)
ax.set_xlabel("Nilai Ujian (Domain 0 - 100)")
ax.set_ylabel("Derajat Keanggotaan \u03bc(x)")
ax.set_xlim(0, 100)
ax.set_ylim(-0.05, 1.05)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper right")

# Tampilkan plot ke Streamlit
st.pyplot(fig)

st.markdown("---")

# --- 5. PERHITUNGAN DERAJAT KEANGGOTAAN ---
st.subheader("🔢 Hasil Perhitungan Derajat Keanggotaan")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📉 Kategori Rendah (\u03bc Rendah)", value=f"{u_rendah:.2f}")
with col2:
    st.metric(label="📊 Kategori Sedang (\u03bc Sedang)", value=f"{u_sedang:.2f}")
with col3:
    st.metric(label="📈 Kategori Tinggi (\u03bc Tinggi)", value=f"{u_tinggi:.2f}")

st.markdown("---")

# --- 6. INTERPRETASI HASIL ---
st.subheader("💡 Interpretasi Hasil")

# Mencari kategori dengan derajat keanggotaan tertinggi (dominan)
kategori_list = [("Rendah", u_rendah), ("Sedang", u_sedang), ("Tinggi", u_tinggi)]
kategori_dominan = max(kategori_list, key=lambda item: item[1])

if kategori_dominan[1] == 0:
    st.info(f"Nilai ujian **{nilai_input}** tidak masuk ke dalam kategori manapun.")
else:
    st.success(
        f"Berdasarkan nilai ujian **{nilai_input}**, mahasiswa tersebut secara dominan berada pada kategori **{kategori_dominan[0]}** "
        f"dengan derajat keanggotaan sebesar **{kategori_dominan[1]:.2f}**."
    )
