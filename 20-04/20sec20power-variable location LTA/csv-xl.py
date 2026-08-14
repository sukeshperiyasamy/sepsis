import os
from openpyxl import Workbook

# Get current folder
folder_path = os.path.dirname(os.path.abspath(__file__))

print("Working Folder:", folder_path, "\n")

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".csv"):
        csv_path = os.path.join(folder_path, filename)
        excel_filename = os.path.splitext(filename)[0] + ".xlsx"
        excel_path = os.path.join(folder_path, excel_filename)

        try:
            print("Converting:", filename)

            wb = Workbook()
            ws = wb.active

            with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
                for row_idx, line in enumerate(f, start=1):
                    # Split by comma (change to '\t' if tab separated)
                    columns = line.strip().split(",")
                    for col_idx, value in enumerate(columns, start=1):
                        ws.cell(row=row_idx, column=col_idx, value=value)

            wb.save(excel_path)

            # Delete CSV only after Excel saved
            if os.path.exists(excel_path):
                os.remove(csv_path)
                print("Converted and deleted:", filename)
            else:
                print("Failed to create Excel for:", filename)

        except Exception as e:
            print("Error processing", filename)
            print("Reason:", str(e))

print("\nConversion completed.")