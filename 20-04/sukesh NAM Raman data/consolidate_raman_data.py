import os
import pandas as pd
from pathlib import Path
import glob

# Base directory containing all folders
base_dir = r"c:\Users\sukes\Downloads\sukesh NAM Raman data"

# Define folder processing order (based on integration time)
folders = [
    "5sec-power5-80 and 2set",
    "10sec-power5-80-2set",
    "15sec-power5-80andset2",
    "20sec-power5-80and set2",
    "25sec-power5-80 and set2",
    "NAM-15secs and power15-75-2sets",
    "MB 1ugml"
]

def extract_laser_power(file_path):
    """Extract laser power level from CSV file metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('laser_powerlevel,'):
                    power = line.split(',')[1].strip()
                    return int(float(power))
    except Exception as e:
        print(f"Error reading power from {file_path}: {e}")
    return None

def extract_raman_data(file_path):
    """Extract Raman Shift and intensity data from CSV file"""
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
            print(f"No 'Raman Shift' header found in {file_path}")
            return None, None
        
        # Read data starting from the line after header
        data_lines = []
        for line in lines[header_line_idx + 1:]:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                try:
                    # Extract Raman Shift (column 4, index 3) and Dark Subtracted (column 12, index 11)
                    raman_shift = float(parts[3])
                    intensity = float(parts[11])
                    data_lines.append((raman_shift, intensity))
                except (ValueError, IndexError):
                    continue
        
        if not data_lines:
            return None, None
        
        raman_shifts, intensities = zip(*data_lines)
        return list(raman_shifts), list(intensities)
    
    except Exception as e:
        print(f"Error extracting data from {file_path}: {e}")
        return None, None

# Dictionary to store power -> (file_path, raman_shift, intensity) mapping
power_data = {}
raman_shift_master = None

print("Processing files...")

# Process folders in order
for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue
    
    # Get all CSV files in the folder, sorted
    csv_files = sorted(glob.glob(os.path.join(folder_path, "*.csv")))
    
    for csv_file in csv_files:
        print(f"Processing: {os.path.basename(csv_file)}")
        
        # Extract laser power
        power = extract_laser_power(csv_file)
        if power is None:
            print(f"  Skipping - no power level found")
            continue
        
        # Check if this power already exists (keep only first occurrence)
        if power in power_data:
            print(f"  Skipping - power {power} already recorded")
            continue
        
        # Extract Raman data
        raman_shift, intensity = extract_raman_data(csv_file)
        if raman_shift is None or intensity is None:
            print(f"  Skipping - could not extract data")
            continue
        
        # Store the first Raman Shift values
        if raman_shift_master is None:
            raman_shift_master = raman_shift
            print(f"  Using this file for master Raman Shift values")
        
        # Store the power data
        power_data[power] = intensity
        print(f"  Added power {power} with {len(intensity)} data points")

# Create consolidated DataFrame
print("\nCreating consolidated Excel sheet...")

if raman_shift_master is None:
    print("Error: No valid data found!")
    exit(1)

# Sort powers in ascending order
sorted_powers = sorted(power_data.keys())
print(f"Powers found: {sorted_powers}")

# Create DataFrame with proper structure:
# - Column A: Empty
# - Row 1: "LASER power X" for each power
# - Row 2: "Raman Shift" for each column
# - Row 3+: Raman Shift values

# Prepare header rows
header_row1 = ['']  # Column A empty
header_row2 = ['']  # Column A empty

for power in sorted_powers:
    header_row1.append(f'LASER power {power}')
    header_row2.append('Raman Shift')

# Prepare data rows
data_rows = []
for i in range(len(raman_shift_master)):
    row = ['']  # Column A empty
    for power in sorted_powers:
        row.append(power_data[power][i])
    data_rows.append(row)

# Combine all rows
all_rows = [header_row1, header_row2] + data_rows

# Create DataFrame without headers (we're managing them manually)
df = pd.DataFrame(all_rows)

# Save to Excel
output_file = os.path.join(base_dir, "Combined_Raman.xlsx")
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Combined_Raman', index=False, header=False)

print(f"\nSuccess! Consolidated data saved to: {output_file}")
print(f"Total columns: {len(df.columns)} (1 empty + {len(sorted_powers)} power levels)")
print(f"Total rows: {len(df)} (2 header rows + {len(raman_shift_master)} data rows)")
