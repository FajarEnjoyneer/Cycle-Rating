import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import stumpy

ref_df = pd.read_excel("referensi.xlsx")
sample_df = pd.read_excel("../sample/STR6.xlsx")

ref_df['Timestamp'] = pd.to_datetime(ref_df['Timestamp'])
sample_df['Timestamp'] = pd.to_datetime(sample_df['Timestamp'])

ref_df['Pressure'] = pd.to_numeric(ref_df['Pressure'], errors='coerce')
sample_df['Pressure'] = pd.to_numeric(sample_df['Pressure'], errors='coerce')

threshold = 0.01
sample_df['Pressure_Diff'] = sample_df['Pressure'].diff()

rise_index = sample_df[sample_df['Pressure_Diff'] > threshold].index[0]
rise_timestamp_sample = sample_df.loc[rise_index, 'Timestamp']
first_timestamp_ref = ref_df['Timestamp'].iloc[0]
time_diff = first_timestamp_ref - rise_timestamp_sample
sample_df['Timestamp'] = sample_df['Timestamp'] + time_diff
sample_df.drop(columns='Pressure_Diff', inplace=True)

def cycle_count(Q_df, T_df):
    Q_z_norm = stumpy.core.z_norm(Q_df['Pressure'].values)
    similarity_scores = {"Sample": []}
    matches = stumpy.match(Q_df['Pressure'].values, T_df['Pressure'].values)

    for match_distance, match_idx in matches:
        match_z_norm = stumpy.core.z_norm(T_df['Pressure'].values[match_idx:match_idx + len(Q_df)])
        cosine_similarity = np.dot(Q_z_norm, match_z_norm) / (np.linalg.norm(Q_z_norm) * np.linalg.norm(match_z_norm)) * 100
        match_idx = int(match_idx)
        cosine_similarity = float(cosine_similarity)
        cycle_start_ts = T_df.iloc[match_idx]['Timestamp']
        similarity_scores["Sample"].append({
            "cycle": match_idx + 1,
            "ts": cycle_start_ts,
            "score": format(cosine_similarity, ".2f")
        })
    similarity_scores["Sample"].sort(key=lambda x: x['cycle'])
    return similarity_scores
cycle_results = cycle_count(ref_df, sample_df)
print("Cycle Count Results:", cycle_results)
plt.figure(figsize=(14, 8))
plt.plot(ref_df['Timestamp'], ref_df['Pressure'], label='Reference Data', color='blue', linewidth=2)
plt.plot(sample_df['Timestamp'], sample_df['Pressure'], label='Sample Data (Aligned)', color='orange', linestyle='--')
for match in cycle_results["Sample"]:
    plt.axvline(x=match['ts'], color='green', linestyle=':', alpha=0.6)
    plt.text(match['ts'], max(sample_df['Pressure']), f"Cycle {match['cycle']} ({match['score']}%)",
             rotation=90, verticalalignment='bottom', color='green')
plt.title('Aligned Comparison of Reference and Sample Pressure Data with Cycle Count')
plt.xlabel('Timestamp')
plt.ylabel('Pressure (bar)')
plt.xticks(rotation=45) 
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()
