import os
import pandas as pd
from pathlib import Path
import glob

# Folder containing the CSV files
folder_path = r"C:\Users\sukes\Downloads\sukesh NAM Raman data\25sec-power5-80 and set2"

def extract_power_from_csv(file_path):
    """Extract laser power from the CSV file (around line 40 with 'laser_powerlevel')"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('laser_powerlevel,'):
                    power = line.split(',')[1].strip()
                    return int(float(power))
    except Exception as e:
        print(f"Error reading power from {file_path}: {e}")
    return None

def extract_raman_shift_from_csv(file_path):
    """Extract Raman Shift data from column D (index 3) starting around row 100"""
    try:
        # Find the line where data starts (after the header with 'Raman Shift')
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Find the header line
        header_line_idx = None
        for idx, line in enumerate(lines):
            if 'Raman Shift' in line:
                header_line_idx = idx
                break
        
        if header_line_idx is None:
            return None
        
        # Read Raman Shift values from column 4 (index 3) starting from next line
        raman_values = []
        for line in lines[header_line_idx + 1:]:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                try:
                    # Column D (index 3) contains Raman Shift
                    raman_shift = float(parts[3])
                    raman_values.append(raman_shift)
                except (ValueError, IndexError):
                    continue
        
        return raman_values if raman_values else None
    
    except Exception as e:
        print(f"Error extracting Raman data from {file_path}: {e}")
        return None

# Dictionary to store power -> raman_shift_values
power_data = {}

print("Processing CSV files...")
print(f"Folder: {folder_path}\n")

# Get all CSV files in the folder, sorted
csv_files = sorted(glob.glob(os.path.join(folder_path, "*.csv")))

# Process each file
for csv_file in csv_files:
    print(f"Processing: {os.path.basename(csv_file)}")
    
    # Extract laser power
    power = extract_power_from_csv(csv_file)
    if power is None:
        print(f"  Skipping - no power value found")
        continue
    
    print(f"  Found power: {power}")
    
    # Check if this power already exists (keep only first occurrence)
    if power in power_data:
        print(f"  Skipping - power {power} already recorded")
        continue
    
    # Extract Raman Shift data
    raman_values = extract_raman_shift_from_csv(csv_file)
    if raman_values is None or len(raman_values) == 0:
        print(f"  Skipping - no Raman data found")
        continue
    
    # Store the data
    power_data[power] = raman_values
    print(f"  Added power {power} with {len(raman_values)} data points")

# Create the consolidated Excel sheet
print("\nCreating Combined_Raman Excel sheet...")

if not power_data:
    print("Error: No valid data found!")
    exit(1)

# Sort powers in ascending order
sorted_powers = sorted(power_data.keys())
print(f"Powers found: {sorted_powers}")

# Determine the maximum number of rows needed
max_rows = max(len(power_data[p]) for p in sorted_powers)
print(f"Maximum data rows: {max_rows}")

# Create the data structure:
# Row 1: Empty in A, then power values
# Row 2: Empty in A, then "Raman Shift" labels
# Row 3+: Empty in A, then Raman Shift values

all_rows = []

# Row 1: Power values
row1 = ['']  # Column A empty
for power in sorted_powers:
    row1.append(power)
all_rows.append(row1)

# Row 2: "Raman Shift" labels
row2 = ['']  # Column A empty
for power in sorted_powers:
    row2.append('Raman Shift')
all_rows.append(row2)

# Rows 3+: Raman Shift data
for i in range(max_rows):
    row = ['']  # Column A empty
    for power in sorted_powers:
        values = power_data[power]
        if i < len(values):
            row.append(values[i])
        else:
            row.append('')  # Empty if this power has fewer rows
    all_rows.append(row)

# Create DataFrame
df = pd.DataFrame(all_rows)

# Save to Excel
output_file = os.path.join(os.path.dirname(folder_path), "25sec.xlsx")
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='25sec', index=False, header=False)

print(f"\n{'='*80}")
print(f"✓ Success! Consolidated data saved to:")
print(f"  {output_file}")
print(f"{'='*80}")
print(f"Structure:")
print(f"  - Column A: Empty")
print(f"  - Columns B-{chr(65 + len(sorted_powers))}: Power levels {sorted_powers}")
print(f"  - Total rows: {len(all_rows)} (1 power row + 1 header row + {max_rows} data rows)")
print(f"{'='*80}")
