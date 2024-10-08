import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ref_df = pd.read_excel("referensi.xlsx")
sample_df = pd.read_excel("data_cleaned.xlsx")

ref_df['Timestamp'] = pd.to_datetime(ref_df['Timestamp'])
sample_df['Timestamp'] = pd.to_datetime(sample_df['Timestamp'])

ref_df['Pressure'] = pd.to_numeric(ref_df['Pressure'], errors='coerce')
sample_df['Pressure'] = pd.to_numeric(sample_df['Pressure'], errors='coerce')

threshold = 0.02
sample_df['Pressure_Diff'] = sample_df['Pressure'].diff()

rise_index = sample_df[sample_df['Pressure_Diff'] > threshold].index[0]
rise_timestamp_sample = sample_df.loc[rise_index, 'Timestamp']
first_timestamp_ref = ref_df['Timestamp'].iloc[0]
time_diff = first_timestamp_ref - rise_timestamp_sample
sample_df['Timestamp'] = sample_df['Timestamp'] + time_diff
sample_df.drop(columns='Pressure_Diff', inplace=True)

plt.figure(figsize=(14, 8))
plt.plot(ref_df['Timestamp'], ref_df['Pressure'], label='Reference Data', color='blue', linewidth=2)
plt.plot(sample_df['Timestamp'], sample_df['Pressure'], label='Sample Data (Aligned)', color='orange', linestyle='--')
plt.title('Aligned Comparison of Reference and Sample Pressure Data')
plt.xlabel('Timestamp')
plt.ylabel('Pressure (bar)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
