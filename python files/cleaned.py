import os
import pandas as pd


def fmt(val):
    """Format numeric value: show as int if whole number, else as-is."""
    try:
        f = float(val)
        return str(int(f)) if f == int(f) else str(f)
    except (TypeError, ValueError):
        return str(val)


# Get root folder (same directory as this script)
folder_path = os.path.dirname(os.path.abspath(__file__))

print("Working Folder:", folder_path, "\n")

# ─────────────────────────────────────────────────────────────
# STEP 1: CLEAN  — extract metadata + Raman data into new file
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Cleaning files...")
print("=" * 60)

clean_ok = 0
clean_err = 0
# Track: original path -> temp cleaned path (for steps 2 & 3)
cleaned_map = {}   # { original_path: temp_cleaned_path }

for root, dirs, files in os.walk(folder_path):
    for file in sorted(files):
        if not file.endswith(".xlsx") or file.startswith(("cleaned_", "sec-", "~$")):
            continue

        file_path = os.path.join(root, file)
        rel_path  = os.path.relpath(file_path, folder_path)
        print(f"  Cleaning: {rel_path}")

        try:
            df = pd.read_excel(file_path, header=None)

            # ---- Extract metadata cells ----
            a20 = df.iloc[19, 0];  b20 = df.iloc[19, 1]  # integration times(sec)
            a21 = df.iloc[20, 0];  b21 = df.iloc[20, 1]  # integration times unit
            a40 = df.iloc[39, 0];  b40 = df.iloc[39, 1]  # laser_powerlevel

            # ---- Extract Raman data (index 98 includes the header row) ----
            raman_shift = df.iloc[98:2147, 3].reset_index(drop=True)
            dark_sub    = df.iloc[98:2147, 7].reset_index(drop=True)

            max_len = max(len(raman_shift), 3)
            clean_df = pd.DataFrame(index=range(max_len), columns=[0, 1, 2, 3])

            clean_df.iloc[0, 0] = a20;  clean_df.iloc[0, 1] = b20
            clean_df.iloc[1, 0] = a21;  clean_df.iloc[1, 1] = b21
            clean_df.iloc[2, 0] = a40;  clean_df.iloc[2, 1] = b40
            clean_df.iloc[:len(raman_shift), 2] = raman_shift.values
            clean_df.iloc[:len(dark_sub),    3] = dark_sub.values

            temp_path = os.path.join(root, f"cleaned_{file}")
            clean_df.to_excel(temp_path, index=False, header=False)

            print(f"    -> cleaned_{file}  ({len(raman_shift)} rows)")
            cleaned_map[file_path] = temp_path
            clean_ok += 1

        except Exception as e:
            print(f"    ERROR: {e}")
            clean_err += 1

print(f"\nStep 1 result: {clean_ok} cleaned, {clean_err} failed.\n")

# ─────────────────────────────────────────────────────────────
# STEP 2: RENAME  — sec-<b1>_power-<b3>_i-<b2>.xlsx
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 2: Renaming cleaned files...")
print("=" * 60)

rename_ok = 0
rename_err = 0
# Track: original path -> final renamed path (for step 3 verification)
renamed_map = {}   # { original_path: final_renamed_path }
# Per-folder name collision counter
used_names = {}    # { folder: { base_name: count } }

for orig_path, temp_path in cleaned_map.items():
    rel_path = os.path.relpath(temp_path, folder_path)
    try:
        df2 = pd.read_excel(temp_path, header=None)

        b1 = fmt(df2.iloc[0, 1])   # integration times(sec)
        b2 = fmt(df2.iloc[1, 1])   # integration times unit  (i)
        b3 = fmt(df2.iloc[2, 1])   # laser_powerlevel

        base_name = f"sec-{b1}_power-{b3}_i-{b2}"
        folder_key = os.path.dirname(temp_path)

        if folder_key not in used_names:
            used_names[folder_key] = {}

        if base_name not in used_names[folder_key]:
            used_names[folder_key][base_name] = 1
            new_filename = base_name + ".xlsx"
        else:
            used_names[folder_key][base_name] += 1
            new_filename = f"{base_name}_{used_names[folder_key][base_name]}.xlsx"

        final_path = os.path.join(folder_key, new_filename)
        os.rename(temp_path, final_path)

        print(f"  {rel_path}")
        print(f"    -> {new_filename}")
        renamed_map[orig_path] = final_path
        rename_ok += 1

    except Exception as e:
        print(f"  ERROR renaming {rel_path}: {e}")
        rename_err += 1

print(f"\nStep 2 result: {rename_ok} renamed, {rename_err} failed.\n")

# ─────────────────────────────────────────────────────────────
# STEP 3: VERIFY + DELETE originals
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 3: Verifying renamed files, then deleting originals...")
print("=" * 60)

delete_ok  = 0
delete_err = 0
skipped    = []

for orig_path, final_path in renamed_map.items():
    orig_rel  = os.path.relpath(orig_path,  folder_path)
    final_rel = os.path.relpath(final_path, folder_path)

    # Check renamed file actually exists on disk
    if not os.path.exists(final_path):
        print(f"  MISSING  {final_rel} — original kept: {orig_rel}")
        skipped.append(orig_rel)
        delete_err += 1
        continue

    # Check renamed file is non-empty
    if os.path.getsize(final_path) == 0:
        print(f"  EMPTY    {final_rel} — original kept: {orig_rel}")
        skipped.append(orig_rel)
        delete_err += 1
        continue

    # Quick row-count sanity check
    try:
        df_check = pd.read_excel(final_path, header=None)
        if len(df_check) < 3:
            raise ValueError(f"only {len(df_check)} rows found")
    except Exception as e:
        print(f"  CORRUPT  {final_rel} ({e}) — original kept: {orig_rel}")
        skipped.append(orig_rel)
        delete_err += 1
        continue

    # All checks passed — safe to delete original
    os.remove(orig_path)
    print(f"  OK  {final_rel}  -> deleted {os.path.basename(orig_path)}")
    delete_ok += 1

# ─────────────────────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────────────────────
print(f"\n{'=' * 60}")
print(f"STEP 1  Cleaned : {clean_ok:>3} ok,  {clean_err} failed")
print(f"STEP 2  Renamed : {rename_ok:>3} ok,  {rename_err} failed")
print(f"STEP 3  Deleted : {delete_ok:>3} originals removed,  {delete_err} kept (see above)")
if skipped:
    print("\nOriginals kept (manual check needed):")
    for s in skipped:
        print(f"  - {s}")
print("=" * 60)