#!/usr/bin/env python3
"""
Convert Lipid A MOL file to ORCA input files
ORCA is a free alternative to Gaussian - download from:
https://orcaforum.kofo.mpg.de/

Generates:
  1. lipidA_opt.inp - Geometry optimization
  2. lipidA_freq.inp - Frequency + Raman calculation
"""

from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

print("=" * 78)
print("ORCA Input Generator for Lipid A (Free Gaussian Alternative)")
print("=" * 78)

# Read MOL file
print("\n[1/3] Reading LipidA_proxy_Ecoli_O111B4.mol...")
mol = Chem.MolFromMolFile("LipidA_proxy_Ecoli_O111B4.mol", removeHs=False)

if mol is None:
    print("ERROR: Could not read MOL file")
    exit(1)

print(f"✓ Loaded molecule with {mol.GetNumAtoms()} atoms")

# Get 3D coordinates
conf = mol.GetConformer()

# Get molecular properties
formula = Chem.rdMolDescriptors.CalcMolFormula(mol)
charge = Chem.GetFormalCharge(mol)
multiplicity = 1

print(f"  Formula: {formula}")
print(f"  Charge: {charge}")
print(f"  Multiplicity: {multiplicity}")

# ==============================================================================
# STEP 1: Generate Geometry Optimization Input
# ==============================================================================
print("\n[2/3] Generating lipidA_opt.inp (STEP 1: Geometry Optimization)...")

opt_filename = "lipidA_opt.inp"
with open(opt_filename, 'w') as f:
    # ORCA input format
    f.write("# Lipid A proxy - Geometry Optimization\n")
    f.write("# Representative of E. coli O111:B4 Lipid A\n")
    f.write("# B3LYP/6-31G(d) with D3BJ dispersion\n\n")
    
    f.write("! B3LYP 6-31G(d) D3BJ Opt TightSCF\n")
    f.write("! PAL8        # Use 8 CPU cores\n\n")
    
    f.write("%maxcore 2000  # 2GB per core (adjust based on your RAM)\n\n")
    
    # Charge and multiplicity
    f.write(f"* xyz {charge} {multiplicity}\n")
    
    # Coordinates
    for atom in mol.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        symbol = atom.GetSymbol()
        f.write(f"{symbol:2s}  {pos.x:12.6f}  {pos.y:12.6f}  {pos.z:12.6f}\n")
    
    f.write("*\n")

print(f"✓ {opt_filename} created")

# ==============================================================================
# STEP 2: Generate Frequency + Raman Input
# ==============================================================================
print("\n[3/3] Generating lipidA_freq.inp (STEP 2: Frequency + Raman)...")

freq_filename = "lipidA_freq.inp"
with open(freq_filename, 'w') as f:
    f.write("# Lipid A proxy - Frequency and Raman Calculation\n")
    f.write("# Representative of E. coli O111:B4 Lipid A\n")
    f.write("# Uses optimized geometry from lipidA_opt.xyz\n\n")
    
    f.write("! B3LYP 6-31G(d) D3BJ Freq NumFreq\n")
    f.write("! PAL8\n\n")
    
    f.write("%maxcore 2000\n\n")
    
    # Read geometry from optimized structure
    f.write(f'* xyzfile {charge} {multiplicity} lipidA_opt.xyz\n')

print(f"✓ {freq_filename} created")

# ==============================================================================
# Summary
# ==============================================================================
print("\n" + "=" * 78)
print("ORCA INPUT FILES GENERATED")
print("=" * 78)

print("\n📥 DOWNLOAD ORCA (FREE):")
print("━" * 78)
print("  Website: https://orcaforum.kofo.mpg.de/")
print("  License: Free for academic use")
print("  Platforms: Windows, Linux, macOS")
print("━" * 78)

print("\n📋 FILE OVERVIEW:")
print("━" * 78)
print(f"  1. {opt_filename}")
print("     → STEP 1: Geometry optimization")
print("     → Run: orca lipidA_opt.inp > lipidA_opt.out")
print("     → Generates: lipidA_opt.xyz (optimized geometry)")
print(f"\n  2. {freq_filename}")
print("     → STEP 2: Frequency calculation")
print("     → Run AFTER optimization completes")
print("     → Run: orca lipidA_freq.inp > lipidA_freq.out")
print("━" * 78)

print("\n⚙️  COMPUTATIONAL SETTINGS:")
print("━" * 78)
print(f"  Method:       B3LYP/6-31G(d)")
print(f"  Dispersion:   D3BJ")
print(f"  Charge:       {charge}")
print(f"  Multiplicity: {multiplicity}")
print(f"  CPUs:         8 cores (adjust PAL8 if needed)")
print(f"  Memory:       2GB per core (adjust %maxcore)")
print("━" * 78)

print("\n✅ WORKFLOW:")
print("━" * 78)
print("  1. Install ORCA (free download)")
print("  2. Run: orca lipidA_opt.inp > lipidA_opt.out")
print("  3. Check lipidA_opt.out for 'OPTIMIZATION RUN DONE'")
print("  4. Run: orca lipidA_freq.inp > lipidA_freq.out")
print("  5. Extract frequencies from lipidA_freq.out")
print("━" * 78)

print("\n💡 ALTERNATIVE: Use online services if you can't install ORCA")
print("━" * 78)
print("  • ChemCompute: https://chemcompute.carlboettiger.info/")
print("  • WebMO: https://www.webmo.net/ (demo version)")
print("  • XSEDE: Academic supercomputer access")
print("━" * 78)

print("\n✅ All files ready")
print("=" * 78)
