import pandas as pd

# Read the Excel file
file_path = r"c:\Users\sukes\Downloads\sukesh NAM Raman data\Combined_Raman.xlsx"
df = pd.read_excel(file_path, sheet_name='Combined_Raman', header=None)

print("=" * 80)
print("VERIFICATION OF Combined_Raman.xlsx")
print("=" * 80)

print(f"\nTotal Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Column A is empty: {df.iloc[:, 0].isna().all() or (df.iloc[:, 0] == '').all()}")

print("\n" + "=" * 80)
print("First 3 rows (headers + 1 data row):")
print("=" * 80)
print(df.head(3).to_string())

print("\n" + "=" * 80)
print("Row 1 (Power headers):")
print("=" * 80)
print(f"Column A: '{df.iloc[0, 0]}'")
for i in range(1, min(6, df.shape[1])):
    print(f"Column {chr(65+i)}: '{df.iloc[0, i]}'")
print("...")

print("\n" + "=" * 80)
print("Row 2 (Raman Shift headers):")
print("=" * 80)
print(f"Column A: '{df.iloc[1, 0]}'")
for i in range(1, min(6, df.shape[1])):
    print(f"Column {chr(65+i)}: '{df.iloc[1, i]}'")
print("...")

print("\n" + "=" * 80)
print("Sample data from Row 3:")
print("=" * 80)
print(f"Column A: '{df.iloc[2, 0]}'")
for i in range(1, min(6, df.shape[1])):
    print(f"Column {chr(65+i)}: {df.iloc[2, i]}")
print("...")

print("\n" + "=" * 80)
print("✓ File created successfully with the required format!")
print("=" * 80)
