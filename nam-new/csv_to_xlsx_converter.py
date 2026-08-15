#!/usr/bin/env python3
"""
CSV to XLSX Converter with Comprehensive Verification
Converts all CSV files to XLSX, verifies integrity, and deletes originals only if all pass.
Special handling for Raman spectroscopy CSV files with metadata.
"""

import os
import pandas as pd
from pathlib import Path
import time
import sys
from datetime import datetime
from tqdm import tqdm

# Configuration
BASE_DIR = r"c:\Users\sukes\Downloads\nam-new"
REPORT_XLSX = os.path.join(BASE_DIR, "conversion_report.xlsx")
REPORT_TXT = os.path.join(BASE_DIR, "conversion_report.txt")

# Global results storage
conversion_results = []
start_time = time.time()


def find_csv_files(base_dir):
    """Recursively find all CSV files, excluding ignored files."""
    csv_files = []

    for root, dirs, files in os.walk(base_dir):
        # Skip .claude directory
        if '.claude' in dirs:
            dirs.remove('.claude')

        for file in files:
            # Only process .csv files
            if file.lower().endswith('.csv'):
                full_path = os.path.join(root, file)
                csv_files.append(full_path)

    return sorted(csv_files)


def find_header_row(csv_path):
    """Find the row number where actual data header starts."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            # Header row contains "Pixel" as first column
            if line.startswith('Pixel,'):
                return line_num
    return None


def convert_csv_to_xlsx(csv_path):
    """Convert single CSV to XLSX, handling metadata."""
    try:
        # Find header row
        header_row = find_header_row(csv_path)
        if header_row is None:
            return None, None, "Could not find data header row (Pixel column)"

        # Read CSV skipping metadata rows, using header row
        df = pd.read_csv(
            csv_path,
            encoding='utf-8',
            skiprows=header_row,
            keep_default_na=False
        )

        # Remove trailing empty column if exists
        if df.columns[-1] == '' or df.iloc[:, -1].isna().all():
            df = df.iloc[:, :-1]

        # Create XLSX path (same location, .xlsx extension)
        xlsx_path = csv_path.replace('.csv', '.xlsx')

        # Write to XLSX
        with pd.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')

        return xlsx_path, df.shape, None

    except Exception as e:
        return None, None, str(e)


def verify_conversion(csv_path, xlsx_path, csv_shape):
    """Verify XLSX matches CSV exactly."""
    try:
        # Find header row for CSV
        header_row = find_header_row(csv_path)

        # Read CSV
        csv_df = pd.read_csv(
            csv_path,
            encoding='utf-8',
            skiprows=header_row,
            keep_default_na=False
        )

        # Remove trailing empty column if exists
        if csv_df.columns[-1] == '' or csv_df.iloc[:, -1].isna().all():
            csv_df = csv_df.iloc[:, :-1]

        # Read XLSX
        xlsx_df = pd.read_excel(xlsx_path, engine='openpyxl', sheet_name='Data', keep_default_na=False)

        # Get shapes
        csv_rows, csv_cols = csv_df.shape
        xlsx_rows, xlsx_cols = xlsx_df.shape

        # Compare shapes
        if csv_rows != xlsx_rows or csv_cols != xlsx_cols:
            error_msg = f"Shape mismatch: CSV({csv_rows}x{csv_cols}) vs XLSX({xlsx_rows}x{xlsx_cols})"
            return False, csv_rows, csv_cols, xlsx_rows, xlsx_cols, error_msg

        # Compare column names
        if list(csv_df.columns) != list(xlsx_df.columns):
            error_msg = f"Column names mismatch"
            return False, csv_rows, csv_cols, xlsx_rows, xlsx_cols, error_msg

        # Compare values (convert to string to handle numeric precision)
        comparison = csv_df.astype(str) == xlsx_df.astype(str)
        if not comparison.all().all():
            # Find first mismatch
            mismatch_indices = (comparison == False).stack()
            if mismatch_indices.any():
                mismatch_row = mismatch_indices.idxmax()[0]
                mismatch_col = mismatch_indices.idxmax()[1]
                error_msg = f"Value mismatch at row {mismatch_row}, column '{mismatch_col}'"
                return False, csv_rows, csv_cols, xlsx_rows, xlsx_cols, error_msg

        return True, csv_rows, csv_cols, xlsx_rows, xlsx_cols, None

    except Exception as e:
        return False, None, None, None, None, str(e)


def process_file(csv_path):
    """Process a single CSV file: convert and verify."""
    rel_path = os.path.relpath(csv_path, BASE_DIR)

    try:
        # Step 1: Convert
        conversion_start = time.time()
        xlsx_path, csv_shape, conversion_error = convert_csv_to_xlsx(csv_path)
        conversion_time = time.time() - conversion_start

        if conversion_error:
            return {
                'file_name': os.path.basename(csv_path),
                'rel_path': rel_path,
                'csv_rows': None,
                'csv_cols': None,
                'xlsx_rows': None,
                'xlsx_cols': None,
                'status': 'FAILED',
                'error': f"Conversion error: {conversion_error}",
                'conversion_time': conversion_time
            }

        # Step 2: Verify
        verify_start = time.time()
        is_valid, csv_rows, csv_cols, xlsx_rows, xlsx_cols, verify_error = verify_conversion(
            csv_path, xlsx_path, csv_shape
        )
        verify_time = time.time() - verify_start

        if verify_error:
            return {
                'file_name': os.path.basename(csv_path),
                'rel_path': rel_path,
                'csv_rows': csv_rows,
                'csv_cols': csv_cols,
                'xlsx_rows': xlsx_rows,
                'xlsx_cols': xlsx_cols,
                'status': 'FAILED',
                'error': f"Verification error: {verify_error}",
                'conversion_time': conversion_time + verify_time
            }

        return {
            'file_name': os.path.basename(csv_path),
            'rel_path': rel_path,
            'csv_rows': csv_rows,
            'csv_cols': csv_cols,
            'xlsx_rows': xlsx_rows,
            'xlsx_cols': xlsx_cols,
            'status': 'PASSED' if is_valid else 'FAILED',
            'error': None,
            'conversion_time': conversion_time + verify_time
        }

    except Exception as e:
        return {
            'file_name': os.path.basename(csv_path),
            'rel_path': rel_path,
            'csv_rows': None,
            'csv_cols': None,
            'xlsx_rows': None,
            'xlsx_cols': None,
            'status': 'FAILED',
            'error': f"Unexpected error: {str(e)}",
            'conversion_time': 0
        }


def generate_xlsx_report(results):
    """Generate conversion report as XLSX."""
    report_df = pd.DataFrame([
        {
            'File Name': r['file_name'],
            'Original Path': r['rel_path'],
            'CSV Rows': r['csv_rows'],
            'CSV Columns': r['csv_cols'],
            'XLSX Rows': r['xlsx_rows'],
            'XLSX Columns': r['xlsx_cols'],
            'Status': r['status'],
            'Error Message': r['error'] if r['error'] else '',
            'Conversion Time (s)': round(r['conversion_time'], 4)
        }
        for r in results
    ])

    with pd.ExcelWriter(REPORT_XLSX, engine='openpyxl') as writer:
        report_df.to_excel(writer, index=False, sheet_name='Conversion Report')

        # Auto-adjust column widths
        worksheet = writer.sheets['Conversion Report']
        for i, col in enumerate(report_df.columns):
            max_len = max(
                report_df[col].astype(str).map(len).max(),
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + i)].width = min(max_len, 50)


def generate_txt_report(results):
    """Generate human-readable text report."""
    total_files = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASSED')
    failed = total_files - passed

    total_time = time.time() - start_time

    report_lines = [
        "=" * 100,
        "CSV TO XLSX CONVERSION REPORT",
        "=" * 100,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Base Directory: {BASE_DIR}",
        "",
        "OVERALL STATISTICS",
        "-" * 100,
        f"Total CSV Files Found: {total_files}",
        f"Successfully Converted & Verified: {passed}",
        f"Failed Conversions: {failed}",
        f"Verification Status: {'ALL PASSED [OK]' if failed == 0 else f'FAILURES FOUND [ERROR] ({failed} failures)'}",
        f"Total Processing Time: {total_time:.2f} seconds",
        "",
    ]

    if failed > 0:
        report_lines.extend([
            "FAILED FILES - DETAILS",
            "-" * 100,
        ])
        for r in results:
            if r['status'] == 'FAILED':
                report_lines.extend([
                    f"File: {r['rel_path']}",
                    f"Error: {r['error']}",
                    ""
                ])

        report_lines.append("ACTION TAKEN: CSV files NOT deleted (failures detected)")
    else:
        report_lines.append("ACTION TAKEN: All files passed verification. CSV files will be deleted.")

    report_lines.extend([
        "",
        "DETAILED FILE LISTING",
        "-" * 100,
    ])

    for i, r in enumerate(results, 1):
        status_icon = "[OK]" if r['status'] == 'PASSED' else "[FAIL]"
        report_lines.append(
            f"{i:3d}. {status_icon} {r['rel_path']}"
        )
        if r['status'] == 'PASSED':
            report_lines.append(
                f"     Rows: {r['csv_rows']} -> {r['xlsx_rows']}, "
                f"Cols: {r['csv_cols']} -> {r['xlsx_cols']}, "
                f"Time: {r['conversion_time']:.3f}s"
            )
        else:
            report_lines.append(f"     ERROR: {r['error']}")

    report_lines.extend([
        "",
        "=" * 100,
    ])

    # Write to file
    with open(REPORT_TXT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))


def delete_csv_files(results):
    """Delete CSV files only if all verifications passed."""
    failed = [r for r in results if r['status'] == 'FAILED']

    if failed:
        print("\n" + "=" * 100)
        print("DELETION ABORTED - FAILURES DETECTED")
        print("=" * 100)
        print(f"\n{len(failed)} file(s) failed verification. Keeping all CSV files for safety.\n")
        for r in failed[:10]:  # Show first 10 failures
            print(f"[FAILED] {r['rel_path']}: {r['error']}")
        if len(failed) > 10:
            print(f"... and {len(failed) - 10} more failures (see conversion_report.txt)")
        print()
        return 0

    print("\n" + "=" * 100)
    print("ALL VERIFICATIONS PASSED - DELETING CSV FILES")
    print("=" * 100 + "\n")

    deleted_count = 0
    for r in results:
        # Find the original CSV path
        csv_path = os.path.join(BASE_DIR, r['rel_path'])

        try:
            if os.path.exists(csv_path):
                os.remove(csv_path)
                deleted_count += 1
                print(f"[DEL] Deleted: {r['rel_path']}")
        except Exception as e:
            print(f"[ERR] Failed to delete: {r['rel_path']} - {str(e)}")

    print(f"\nTotal files deleted: {deleted_count}")
    return deleted_count


def main():
    """Main execution flow."""
    print("\n" + "=" * 100)
    print("CSV TO XLSX CONVERTER WITH VERIFICATION")
    print("=" * 100)
    print(f"\nBase Directory: {BASE_DIR}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Step 1: Find all CSV files
    print("Scanning for CSV files...")
    csv_files = find_csv_files(BASE_DIR)
    total_files = len(csv_files)

    if total_files == 0:
        print("No CSV files found!")
        return

    print(f"Found {total_files} CSV files\n")

    # Step 2: Process each file
    print("Converting and verifying files...\n")

    for csv_path in tqdm(csv_files, desc="Processing", unit="file"):
        result = process_file(csv_path)
        conversion_results.append(result)

    # Step 3: Generate reports
    print("\n\nGenerating reports...")
    generate_xlsx_report(conversion_results)
    generate_txt_report(conversion_results)
    print(f"[OK] Report generated: {REPORT_XLSX}")
    print(f"[OK] Report generated: {REPORT_TXT}")

    # Step 4: Display summary
    passed = sum(1 for r in conversion_results if r['status'] == 'PASSED')
    failed = total_files - passed

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Total CSV Files Processed: {total_files}")
    print(f"Successfully Converted & Verified: {passed}")
    print(f"Failed Conversions: {failed}")
    print(f"Verification Status: {'ALL PASSED [OK]' if failed == 0 else f'FAILURES FOUND [ERROR]'}")

    # Step 5: Delete CSV files if all passed
    deleted_count = delete_csv_files(conversion_results)

    total_time = time.time() - start_time
    print(f"\nTotal Processing Time: {total_time:.2f} seconds")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100 + "\n")

    # Return exit code
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
