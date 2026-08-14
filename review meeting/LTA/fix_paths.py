import json
import glob
import os

files = glob.glob('*.ipynb')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    changed = False
    for cell in data.get('cells', []):
        if cell.get('cell_type') == 'code':
            new_source = []
            for line in cell.get('source', []):
                new_line = line
                if 'PROJECT_DIR =' in line:
                    new_line = 'PROJECT_DIR = r"."\n'
                    changed = True
                elif 'SPECTRA_ROOT' in line and '=' in line and 'C:\\\\' in line:
                    new_line = 'SPECTRA_ROOT = r"all_excel_files"\n'
                    changed = True
                elif 'SIM_FILE' in line and '=' in line and 'C:\\\\' in line:
                    new_line = 'SIM_FILE = r"simdata.xlsx"\n'
                    changed = True
                elif 'OUTPUT_DIR' in line and '=' in line and 'C:\\\\' in line:
                    new_line = 'OUTPUT_DIR = r"output_figures"\n'
                    changed = True
                new_source.append(new_line)
            if new_source != cell.get('source'):
                cell['source'] = new_source
                changed = True
    if changed:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1)
        print(f"Fixed {file}")
