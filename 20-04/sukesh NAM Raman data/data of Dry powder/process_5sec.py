import pandas as pd
import numpy as np
from pathlib import Path

# Set the folder path
folder_path = Path(r"c:\Users\sukes\Downloads\sukesh NAM Raman data\data of Dry powder\5sec-power5-80 and 2set")

# Get all CSV files
csv_files = sorted(folder_path.glob('SP_*.csv'))
print(f'Found {len(csv_files)} CSV files')
print('='*60)

# Read first file to get X1 (Raman shift)
print('Reading Raman shift values from first file...')
df_first = pd.read_csv(csv_files[0], skiprows=98, nrows=2048)
X1 = df_first.iloc[:, 3]  # Column D (Raman Shift)
print(f'✓ X1 data: {len(X1)} points')

# Create output dataframe
output_data = {'X1': X1}

# Process each CSV file to get Y values
print('\nProcessing CSV files:')
for i, csv_file in enumerate(csv_files, 1):
    print(f'  {i:2d}. {csv_file.name}...', end=' ')
    df = pd.read_csv(csv_file, skiprows=98, nrows=2048)
    Y = df.iloc[:, 7]  # Column H (Dark Subtracted)
    output_data[f'Y{i}'] = Y
    print('✓')

# Create DataFrame
df_output = pd.DataFrame(output_data)

print('\n' + '='*60)
print(f'Output DataFrame shape: {df_output.shape}')
print(f'Columns: X1, Y1-Y{len(csv_files)}')

# Save to Excel
output_file = folder_path / 'output.xlsx'
df_output.to_excel(output_file, index=False)

print('='*60)
print('✅ SUCCESS!')
print(f'File saved: {output_file}')
print(f'Contains {df_output.shape[0]} data points × {df_output.shape[1]} columns')
print('='*60)
