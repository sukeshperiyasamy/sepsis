#!/usr/bin/env python3
"""
Convert Lipid A MOL file to Gaussian input files (.gjf)
Generates TWO files following best practices:
  1. lipidA_opt.gjf    - Geometry optimization
  2. lipidA_freq.gjf   - Frequency + Raman calculation
"""

from rdkit import Chem
from rdkit.Chem import AllChem

print("=" * 78)
print("Gaussian Input Generator for Lipid A")
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
multiplicity = 1  # Singlet (all electrons paired)

print(f"  Formula: {formula}")
print(f"  Charge: {charge}")
print(f"  Multiplicity: {multiplicity}")

# ==============================================================================
# STEP 1: Generate Geometry Optimization Input
# ==============================================================================
print("\n[2/3] Generating lipidA_opt.gjf (STEP 1: Geometry Optimization)...")

opt_filename = "lipidA_opt.gjf"
with open(opt_filename, 'w') as f:
    # Link 0 commands
    f.write("%chk=lipidA.chk\n")
    f.write("%mem=8GB\n")
    f.write("%nprocshared=8\n")
    
    # Route section - B3LYP/6-31G(d) with D3BJ dispersion
    f.write("#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt TightSCF\n")
    # Optional: Add solvent model (uncomment if needed)
    # f.write("#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt TightSCF SCRF=(PCM,Solvent=Water)\n")
    f.write("\n")
    
    # Title section
    f.write("Lipid A proxy - geometry optimization\n")
    f.write("Representative of E. coli O111:B4 Lipid A\n")
    f.write("Charge = -2, Multiplicity = 1\n")
    f.write("\n")
    
    # Charge and multiplicity
    f.write(f"{charge} {multiplicity}\n")
    
    # Coordinates
    for atom in mol.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        symbol = atom.GetSymbol()
        f.write(f"{symbol:2s}  {pos.x:12.6f}  {pos.y:12.6f}  {pos.z:12.6f}\n")
    
    # Blank line to terminate
    f.write("\n")

print(f"✓ {opt_filename} created")

# ==============================================================================
# STEP 2: Generate Frequency + Raman Input
# ==============================================================================
print("\n[3/3] Generating lipidA_freq.gjf (STEP 2: Frequency + Raman)...")

freq_filename = "lipidA_freq.gjf"
with open(freq_filename, 'w') as f:
    # Link 0 commands
    f.write("%chk=lipidA.chk\n")
    f.write("%mem=8GB\n")
    f.write("%nprocshared=8\n")
    
    # Route section - reads optimized geometry from checkpoint
    f.write("#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Freq=Raman Geom=AllCheck Guess=Read\n")
    # Optional: Add solvent model (must match optimization if used)
    # f.write("#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Freq=Raman SCRF=(PCM,Solvent=Water) Geom=AllCheck Guess=Read\n")
    f.write("\n")
    
    # Title section (no coordinates needed - reads from .chk)
    f.write("Lipid A proxy - IR and Raman frequencies\n")
    f.write("Representative of E. coli O111:B4 Lipid A\n")
    f.write("\n")

print(f"✓ {freq_filename} created")

# ==============================================================================
# Summary
# ==============================================================================
print("\n" + "=" * 78)
print("GAUSSIAN INPUT FILES GENERATED")
print("=" * 78)

print("\n📋 FILE OVERVIEW:")
print("━" * 78)
print(f"  1. {opt_filename}")
print("     → STEP 1: Geometry optimization")
print("     → Run this FIRST")
print("     → Generates: lipidA.chk (checkpoint file)")
print(f"\n  2. {freq_filename}")
print("     → STEP 2: Frequency + Raman calculation")
print("     → Run AFTER optimization completes")
print("     → Reads geometry from lipidA.chk")
print("━" * 78)

print("\n⚙️  COMPUTATIONAL SETTINGS:")
print("━" * 78)
print(f"  Method:       B3LYP/6-31G(d)")
print(f"  Dispersion:   D3BJ (Grimme's dispersion correction)")
print(f"  Charge:       {charge}")
print(f"  Multiplicity: {multiplicity}")
print(f"  Memory:       8GB")
print(f"  CPUs:         8 cores")
print(f"  SCF:          Tight convergence")
print("━" * 78)

print("\n✅ WORKFLOW:")
print("━" * 78)
print("  1. Submit: g16 lipidA_opt.gjf")
print("  2. Check lipidA_opt.log for 'Stationary point found'")
print("  3. Submit: g16 lipidA_freq.gjf")
print("  4. Check lipidA_freq.log for 'No imaginary frequencies'")
print("  5. Extract Raman spectrum from lipidA_freq.log")
print("━" * 78)

print("\n⚠️  CRITICAL CHECKS:")
print("━" * 78)
print("  ✓ After optimization: Look for 'Optimization completed'")
print("  ✓ After frequency: MUST see 'No imaginary frequencies'")
print("  ✓ If imaginary frequencies found → Re-optimize geometry")
print("━" * 78)

print("\n🔬 EXPECTED RAMAN PEAKS (VALIDATION):")
print("━" * 78)
print("  Region (cm⁻¹)    Assignment")
print("  980–1100         PO₂⁻ stretch")
print("  1060–1130        C–C lipid backbone")
print("  ~1440            CH₂ scissoring")
print("  1540–1580        Amide II")
print("  1640–1680        Amide I")
print("━" * 78)

print("\n💡 OPTIONAL MODIFICATIONS:")
print("━" * 78)
print("  • To add water solvent: Uncomment SCRF lines in both files")
print("  • To adjust memory: Change %mem=8GB to your available RAM")
print("  • To adjust CPUs: Change %nprocshared=8 to your core count")
print("━" * 78)

print("\n✅ All files ready for Gaussian 09/16 submission")
print("=" * 78)
