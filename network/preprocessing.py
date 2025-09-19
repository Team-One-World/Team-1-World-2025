import pandas as pd
import numpy as np


COLUMN_MAPPING = {
    'disposition':       {'kepler': 'koi_disposition', 'k2': 'disposition',   'tess': 'tfopwg_disp'},
    'period':            {'kepler': 'koi_period',      'k2': 'pl_orbper',     'tess': 'pl_orbper'},
    'duration':          {'kepler': 'koi_duration',    'k2': 'pl_trandur',    'tess': 'pl_trandurh'},
    'transit_depth':     {'kepler': 'koi_depth',       'k2': 'pl_trandep',    'tess': 'pl_trandep'},
    'planet_radius':     {'kepler': 'koi_prad',        'k2': 'pl_rade',       'tess': 'pl_rade'},
    'star_temp':         {'kepler': 'koi_steff',       'k2': 'st_teff',       'tess': 'st_teff'},
    'star_radius':       {'kepler': 'koi_srad',        'k2': 'st_rad',        'tess': 'st_rad'},
    'model_snr':         {'kepler': 'koi_model_snr',   'k2': None,            'tess': None},
    'fp_flag_nt':        {'kepler': 'koi_fpflag_nt',   'k2': None,            'tess': None},
    'fp_flag_ss':        {'kepler': 'koi_fpflag_ss',   'k2': None,            'tess': None},
    'fp_flag_co':        {'kepler': 'koi_fpflag_co',   'k2': None,            'tess': None},
    'fp_flag_ec':        {'kepler': 'koi_fpflag_ec',   'k2': None,            'tess': None},
}

TARGET_MAP = {
    'kepler': {'CONFIRMED': 1, 'FALSE POSITIVE': 0},
    'k2':     {'CONFIRMED': 1, 'FALSE POSITIVE': 0, 'CANDIDATE': np.nan},
    'tess':   {'CP': 1, 'FP': 0, 'PC': np.nan}
}


def process_dataset(filepath, source_name):
    """
    Loads, selects, renames, and cleans a single exoplanet dataset.
    
    Args:
        filepath (str): Path to the CSV file.
        source_name (str): The name of the data source ('kepler', 'k2', or 'tess').
        
    Returns:
        pandas.DataFrame: A cleaned and standardized DataFrame, or None if file fails to load.
    """
    print(f"\n--- Processing {source_name.upper()} data from {filepath} ---")
    try:
        df = pd.read_csv(filepath, comment='#')
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}. Please check the path.")
        return None

    processed_cols = {}
    
    # Map and rename columns based on our standard schema
    for standard_name, source_map in COLUMN_MAPPING.items():
        original_name = source_map.get(source_name)
        if original_name and original_name in df.columns:
            processed_cols[standard_name] = df[original_name]
        else:
            processed_cols[standard_name] = pd.Series([np.nan] * len(df), name=standard_name)

    processed_df = pd.DataFrame(processed_cols)

    disposition_map = TARGET_MAP[source_name]
    processed_df['disposition'] = processed_df['disposition'].map(disposition_map)
    
    # Drop rows that are candidates or have no disposition
    processed_df.dropna(subset=['disposition'], inplace=True)
    processed_df['disposition'] = processed_df['disposition'].astype(int)

    processed_df['source'] = source_name
    
    print(f"Finished processing {source_name}. Shape: {processed_df.shape}")
    return processed_df


df_kepler = process_dataset('data/Kepler Data.csv', 'kepler')
df_k2 = process_dataset('data/K2 Data.csv', 'k2')
df_tess = process_dataset('data/TESS Data.csv', 'tess')

dataframes_to_merge = [df for df in [df_kepler, df_k2, df_tess] if df is not None]
if not dataframes_to_merge:
    print("\nNo dataframes to merge. Exiting.")
    exit()

df_merged = pd.concat(dataframes_to_merge, ignore_index=True)

print(f"\n--- Merged all datasets. Total shape: {df_merged.shape} ---")
print("Value counts for the target variable 'disposition':")
print(df_merged['disposition'].value_counts())
print("\nValue counts for the 'source' of the data:")
print(df_merged['source'].value_counts())


print("\n--- Performing final cleaning and imputation on merged data ---")

fp_flag_cols = [col for col in df_merged.columns if 'fp_flag' in col]
df_merged[fp_flag_cols] = df_merged[fp_flag_cols].fillna(0)
print(f"Filled missing values in {fp_flag_cols} with 0.")

numeric_cols = df_merged.select_dtypes(include=np.number).columns.drop('disposition')

print("\nMissing values BEFORE imputation:")
print(df_merged[numeric_cols].isnull().sum().loc[lambda x: x > 0])

for col in numeric_cols:
    if df_merged[col].isnull().any():
        median_val = df_merged[col].median()
        df_merged[col].fillna(median_val, inplace=True)

print("\nMissing values AFTER imputation:")
print(df_merged[numeric_cols].isnull().sum().sum())



df_final = pd.get_dummies(df_merged, columns=['source'], drop_first=True)


output_filename = 'data/Full Data.csv'
df_final.to_csv(output_filename, index=False)

print(f"\n✅ Success! Cleaned and merged data saved to '{output_filename}'")
print("\nFinal DataFrame Info:")
df_final.info()
print("\nFirst 5 rows of the final dataset:")
print(df_final.head())