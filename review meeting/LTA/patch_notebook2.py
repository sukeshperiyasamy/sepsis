import json

def patch_nb(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            new_source = []
            for line in source:
                if "spectra.append({'name': file_path.stem, 'x': x, 'y_raw': y})" in line:
                    new_source.append("        if len(x) > 10:\n")
                    new_source.append("            spectra.append({'name': file_path.stem, 'x': x, 'y_raw': y})\n")
                    new_source.append("        else:\n")
                    new_source.append("            print(f'Skipping {file_path.name} (too few points in range)')\n")
                else:
                    new_source.append(line)
            
            cell['source'] = new_source

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print(f'Updated {filename} skipping empty arrays.')

patch_nb('raman_spectroscopy_analysis.ipynb')
