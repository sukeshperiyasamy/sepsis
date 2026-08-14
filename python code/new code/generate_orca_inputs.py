# generate_orca_inputs.py
import os

# user settings
nprocs = 4
maxcore_mb = 2000
functional_basis_line = "! B3LYP 6-31+G(d,p) Opt Freq TightSCF CPCM(water)"
# change to "! B3LYP 6-31G(d) Opt Freq TightSCF CPCM(water)" if machine limited

# mapping from basename -> (charge, multiplicity)
charge_map = {
    "glucose": (0,1),
    "urea": (0,1),
    "lactic_acid": (0,1),
    "uric_acid": (0,1),
    "cholesterol": (0,1),
    "creatinine": (0,1),
    "alanine": (0,1),
    "glycine": (0,1),
    "ascorbic_acid": (0,1),
    "acetic_acid": (0,1),
}

xyz_files = [f for f in os.listdir('.') if f.lower().endswith('.xyz')]
for xyz in xyz_files:
    base = os.path.splitext(xyz)[0]
    ch, mult = charge_map.get(base, (0,1))
    with open(xyz) as fh:
        xyz_text = fh.read().strip()
    inp_name = base + ".inp"
    with open(inp_name, 'w') as out:
        out.write(functional_basis_line + "\n\n")
        out.write(f"%pal\n nprocs {nprocs}\nend\n\n")
        out.write(f"%maxcore {maxcore_mb}\nend\n\n")
        out.write("%freq\n Raman true\nend\n\n")
        out.write("* xyz {} {}\n".format(ch, mult))
        # If your XYZ includes the header line (#atoms), keep it; else parse coordinates.
        # Try to be safe: if xyz starts with an integer number-of-atoms line, remove it.
        lines = xyz_text.splitlines()
        # detect atom count header
        if len(lines) > 0 and lines[0].strip().split()[0].isdigit() and len(lines[0].split())==1:
            coords = lines[2:]  # skip number and comment line
        else:
            # assume file already has coordinates only
            coords = [ln for ln in lines if ln.strip()]
        for ln in coords:
            out.write(ln + "\n")
        out.write("*\n")
    print("Wrote", inp_name)
