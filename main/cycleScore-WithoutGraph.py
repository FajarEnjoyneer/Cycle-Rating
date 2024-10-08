import pandas as pd
import numpy as np
import stumpy
from datetime import datetime

ref_df = pd.read_excel("referensi.xlsx")
sample_df = pd.read_excel("../sample/BadSample.xlsx")

ref_df['Timestamp'] = pd.to_datetime(ref_df['Timestamp'])
sample_df['Timestamp'] = pd.to_datetime(sample_df['Timestamp'])

ref_df['Pressure'] = pd.to_numeric(ref_df['Pressure'], errors='coerce')
sample_df['Pressure'] = pd.to_numeric(sample_df['Pressure'], errors='coerce')

ref_pressure_z_norm = stumpy.core.z_norm(ref_df['Pressure'].values)
sample_pressure_z_norm = stumpy.core.z_norm(sample_df['Pressure'].values)

matches = stumpy.match(ref_df['Pressure'].values, sample_df['Pressure'].values)

similarity_scores = []

for match_distance, match_idx in matches:
    sample_segment_z_norm = stumpy.core.z_norm(sample_df['Pressure'].values[match_idx:match_idx + len(ref_df)])
    cosine_similarity = np.dot(ref_pressure_z_norm, sample_segment_z_norm) / (np.linalg.norm(ref_pressure_z_norm) * np.linalg.norm(sample_segment_z_norm)) * 100
    match_timestamp = sample_df.iloc[match_idx]['Timestamp']
    similarity_scores.append({
        'cycle': match_idx + 1,
        'timestamp': match_timestamp,
        'score': f"{cosine_similarity:.2f}"
    })

result_df = pd.DataFrame(similarity_scores)

print(result_df)
#result_df.to_excel("cycle_count_results.xlsx", index=False)
