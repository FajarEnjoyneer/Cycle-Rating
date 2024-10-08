import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import numpy as np

# Membaca data dari file Excel
file_path = '../sample/STR4.xlsx'
df = pd.read_excel(file_path)

# Mengonversi kolom 'Timestamp' menjadi tipe datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Menghapus data yang duplikat pada kolom 'Timestamp'
df = df.drop_duplicates(subset='Timestamp')

# Menerapkan Exponential Moving Average (EMA) untuk smoothing
df['EMA Pressure'] = df['Pressure'].ewm(span=10, adjust=False).mean()

# Pastikan timestamp terurut
df = df.sort_values(by='Timestamp')

# Interpolasi Cubic Spline untuk mendapatkan data yang lebih halus
time_numeric = (df['Timestamp'] - df['Timestamp'].min()).dt.total_seconds()  # Mengubah waktu ke detik
cs = CubicSpline(time_numeric, df['EMA Pressure'])

# Membuat data baru untuk interpolasi yang lebih halus (dengan interval lebih kecil)
time_new = np.linspace(time_numeric.min(), time_numeric.max(), 500)
pressure_smooth = cs(time_new)

# Konversi waktu interpolasi ke format datetime
time_new_dt = pd.to_timedelta(time_new, unit='s') + df['Timestamp'].min()

# Plot data aslinya dan yang sudah dihaluskan
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Pressure'], label='Original Pressure', alpha=0.3)
plt.plot(df['Timestamp'], df['EMA Pressure'], label='EMA Smoothed Pressure', color='green')
plt.plot(time_new_dt, pressure_smooth, label='Cubic Spline Interpolation', color='red', linestyle='--')

plt.xlabel('Timestamp')
plt.ylabel('Pressure')
plt.title('Pressure Chart with EMA and Cubic Spline Interpolation')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Tampilkan data setelah pemrosesan
print("Data setelah pemrosesan:")
print(df.head())
print(df['Pressure'].describe())  # Menampilkan statistik dasar kolom Pressure
print("Nilai unik dalam kolom Pressure:")
print(df['Pressure'].unique())  # Menampilkan nilai unik dalam kolom Pressure

# Filter data (contoh: hanya ambil data dengan tekanan lebih dari 0)
filtered_df = df[df['Pressure'] > 0]

# Format kolom Pressure dan EMA Pressure menjadi 2 digit di belakang koma
filtered_df['Pressure'] = filtered_df['Pressure'].round(2)
filtered_df['EMA Pressure'] = filtered_df['EMA Pressure'].round(2)

# Tampilkan hasil filter
print("Data setelah filter:")
print(filtered_df.head())

# Simpan DataFrame yang sudah difilter ke file Excel
output_file_path = 'filtered_pressure_data.xlsx'
try:
    filtered_df.to_excel(output_file_path, index=False)
    print(f"Data yang sudah difilter disimpan ke {output_file_path}")
except Exception as e:
    print(f"Terjadi kesalahan saat menyimpan file: {e}")