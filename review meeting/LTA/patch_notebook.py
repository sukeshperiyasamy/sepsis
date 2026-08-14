import json

def patch_nb(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    changed = False
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            new_source = []
            for line in source:
                new_source.append(line)
                if "cleaned = cleaned.groupby('x', as_index=False)['y'].mean()" in line:
                    new_source.append('\n')
                    new_source.append('    # Filter out Rayleigh peak and high-frequency noise before baseline correction\n')
                    new_source.append('    cleaned = cleaned[(cleaned["x"] >= X_MIN) & (cleaned["x"] <= X_MAX)]\n')
                    changed = True
            
            # Additional check: ALS Lambda might need to be 1e5 or 1e6. 
            # I'll leave it as is, or we can check other bugs.
            cell['source'] = new_source

    if changed:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f'Updated {filename} inline filtering.')
    else:
        print(f'No changes made to {filename}.')

patch_nb('raman_spectroscopy_analysis.ipynb')
