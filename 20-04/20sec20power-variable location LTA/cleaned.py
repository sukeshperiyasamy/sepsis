import os
import pandas as pd

# Get current folder (script location)
folder_path = os.path.dirname(os.path.abspath(__file__))

for file in os.listdir(folder_path):

    # Skip cleaned files and Excel temp files
    if file.endswith(".xlsx") and not file.startswith(("cleaned_", "~$")):

        file_path = os.path.join(folder_path, file)
        print(f"Processing: {file}")

        try:
            df = pd.read_excel(file_path, header=None)

            # ---- Extract required single cells ----
            a20 = df.iloc[19, 0]
            b20 = df.iloc[19, 1]

            a21 = df.iloc[20, 0]
            b21 = df.iloc[20, 1]

            a40 = df.iloc[39, 0]
            b40 = df.iloc[39, 1]

            # ---- Extract Raman data ----
            raman_shift = df.iloc[98:2147, 3].reset_index(drop=True)
            dark_sub = df.iloc[98:2147, 7].reset_index(drop=True)

            # Determine max length
            max_len = max(len(raman_shift), 3)

            # Create empty dataframe
            clean_df = pd.DataFrame(index=range(max_len), columns=[0, 1, 2, 3])

            # Fill A & B values
            clean_df.iloc[0, 0] = a20
            clean_df.iloc[0, 1] = b20

            clean_df.iloc[1, 0] = a21
            clean_df.iloc[1, 1] = b21

            clean_df.iloc[2, 0] = a40
            clean_df.iloc[2, 1] = b40

            # Fill Raman data into column C & D
            clean_df.iloc[:len(raman_shift), 2] = raman_shift
            clean_df.iloc[:len(dark_sub), 3] = dark_sub

            # Save cleaned file WITHOUT header row
            output_file = os.path.join(folder_path, f"cleaned_{file}")
            clean_df.to_excel(output_file, index=False, header=False)

            print(f"Cleaned file saved: cleaned_{file}")

        except Exception as e:
            print(f"Error processing {file}: {e}")

print("\nAll files processed successfully!")