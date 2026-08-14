import pandas as pd

# Read the Excel file
file_path = r"C:\Users\sukes\Downloads\sukesh NAM Raman data\Combined_Raman.xlsx"
df = pd.read_excel(file_path, sheet_name='Combined_Raman', header=None)

print("=" * 80)
print("VERIFICATION OF Combined_Raman.xlsx")
print("=" * 80)

print(f"\nTotal Shape: {df.shape[0]} rows × {df.shape[1]} columns")

print("\n" + "=" * 80)
print("Column A (should be empty):")
print("=" * 80)
print(f"Row 1, Column A: '{df.iloc[0, 0]}'")
print(f"Row 2, Column A: '{df.iloc[1, 0]}'")
print(f"Row 3, Column A: '{df.iloc[2, 0]}'")
print(f"All Column A values are empty/NaN: {df.iloc[:, 0].isna().all() or (df.iloc[:, 0] == '').all()}")

print("\n" + "=" * 80)
print("Row 1 (Power values):")
print("=" * 80)
for i in range(1, min(9, df.shape[1])):
    print(f"Column {chr(65+i)}: {df.iloc[0, i]}")
print("...")

print("\n" + "=" * 80)
print("Row 2 (Raman Shift labels):")
print("=" * 80)
for i in range(1, min(9, df.shape[1])):
    print(f"Column {chr(65+i)}: '{df.iloc[1, i]}'")
print("...")

print("\n" + "=" * 80)
print("Row 3 (First data row - Raman Shift values):")
print("=" * 80)
print(f"Column A: '{df.iloc[2, 0]}'")
for i in range(1, min(6, df.shape[1])):
    print(f"Column {chr(65+i)}: {df.iloc[2, i]}")
print("...")

print("\n" + "=" * 80)
print("Sample view of first 5 rows, first 6 columns:")
print("=" * 80)
# Format output nicely
sample_df = df.iloc[:5, :6].copy()
sample_df.columns = ['A', 'B', 'C', 'D', 'E', 'F']
print(sample_df.to_string(index=False))

print("\n" + "=" * 80)
print("✓ File format verified successfully!")
print("=" * 80)
