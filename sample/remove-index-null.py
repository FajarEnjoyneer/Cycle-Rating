import pandas as pd

# Membaca file Excel
df = pd.read_excel('STR6.xlsx')

# Menghapus baris yang nilai pada kolom 'Pressure' kosong
df_cleaned = df.dropna(subset=['Pressure'])

# Menyimpan hasil ke file Excel baru
df_cleaned.to_excel('STR6.xlsx', index=False)

print("Baris dengan Pressure kosong telah dihapus.")
