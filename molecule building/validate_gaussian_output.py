#!/usr/bin/env python3
"""
Gaussian Output Validator and Raman Data Extractor
Checks optimization/frequency calculations and extracts Raman spectrum

Usage:
  python validate_gaussian_output.py lipidA_opt.log      # Check optimization
  python validate_gaussian_output.py lipidA_freq.log     # Check frequency + extract Raman
"""

import sys
import re
import numpy as np
import matplotlib.pyplot as plt

def check_optimization_log(logfile):
    """Validate geometry optimization completion"""
    print("=" * 78)
    print(f"CHECKING OPTIMIZATION: {logfile}")
    print("=" * 78)
    
    try:
        with open(logfile, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: File {logfile} not found")
        print("   Make sure optimization job has completed")
        return False
    
    # Check for successful optimization
    checks = {
        'Optimization completed': False,
        'Stationary point found': False,
        'Normal termination': False
    }
    
    for key in checks.keys():
        if key in content:
            checks[key] = True
            print(f"✓ Found: '{key}'")
        else:
            print(f"❌ Missing: '{key}'")
    
    # Check for errors
    if 'Error termination' in content:
        print("\n❌ CRITICAL: Error termination detected")
        
        # Common errors
        if 'FormBX had a problem' in content:
            print("   Issue: SCF convergence problem")
            print("   Fix: Add SCF=(XQC,MaxCycle=512) to route section")
        
        if 'Convergence failure' in content:
            print("   Issue: Geometry optimization didn't converge")
            print("   Fix: Add Opt=(CalcFC,MaxCycle=100) to route section")
        
        return False
    
    # Extract final energy
    energy_match = re.search(r'SCF Done.*E\(RB3LYP\)\s*=\s*([-\d.]+)', content)
    if energy_match:
        energy = float(energy_match.group(1))
        print(f"\n📊 Final SCF Energy: {energy:.6f} Hartree")
    
    print("\n" + "=" * 78)
    if all(checks.values()):
        print("✅ OPTIMIZATION SUCCESSFUL")
        print("   → Proceed to frequency calculation: g16 lipidA_freq.gjf")
        print("=" * 78)
        return True
    else:
        print("❌ OPTIMIZATION FAILED OR INCOMPLETE")
        print("   → Review .log file for details")
        print("=" * 78)
        return False

def check_frequency_log(logfile):
    """Validate frequency calculation and extract Raman data"""
    print("=" * 78)
    print(f"CHECKING FREQUENCY CALCULATION: {logfile}")
    print("=" * 78)
    
    try:
        with open(logfile, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: File {logfile} not found")
        print("   Make sure frequency job has completed")
        return False, None, None
    
    # Check for successful completion
    if 'Normal termination' not in content:
        print("❌ CRITICAL: Job did not terminate normally")
        return False, None, None
    
    print("✓ Job terminated normally")
    
    # Check for imaginary frequencies
    imaginary_freqs = []
    freq_pattern = re.compile(r'Frequencies\s*--\s*([-\d.]+(?:\s+[-\d.]+)*)')
    
    for match in freq_pattern.finditer(content):
        freqs = [float(f) for f in match.group(1).split()]
        for f in freqs:
            if f < 0:
                imaginary_freqs.append(f)
    
    if imaginary_freqs:
        print(f"\n❌ WARNING: Found {len(imaginary_freqs)} imaginary frequencies:")
        for f in imaginary_freqs[:5]:  # Show first 5
            print(f"   {f:.2f} cm⁻¹")
        print("\n   This means the geometry is NOT a true minimum!")
        print("   → Re-run optimization with tighter convergence:")
        print("      Opt=(Tight,CalcFC)")
        return False, None, None
    
    print("✓ No imaginary frequencies - geometry is a true minimum")
    
    # Extract Raman data
    print("\n" + "=" * 78)
    print("EXTRACTING RAMAN SPECTRUM DATA")
    print("=" * 78)
    
    frequencies = []
    raman_activities = []
    depolarizations = []
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'Frequencies --' in line:
            freq_values = [float(x) for x in line.split()[2:]]
            
            # Look for corresponding Raman activities
            for j in range(i, min(i+10, len(lines))):
                if 'Raman Activ --' in lines[j]:
                    raman_values = [float(x) for x in lines[j].split()[3:]]
                    frequencies.extend(freq_values)
                    raman_activities.extend(raman_values)
                    break
                
                if 'Depolar' in lines[j]:
                    depol_values = [float(x) for x in lines[j].split()[2:]]
                    depolarizations.extend(depol_values)
    
    frequencies = np.array(frequencies)
    raman_activities = np.array(raman_activities)
    
    if len(frequencies) == 0:
        print("❌ ERROR: Could not extract Raman data")
        print("   Make sure Freq=Raman was specified in route section")
        return False, None, None
    
    print(f"✓ Extracted {len(frequencies)} Raman-active modes")
    print(f"  Frequency range: {frequencies.min():.1f} - {frequencies.max():.1f} cm⁻¹")
    print(f"  Max Raman activity: {raman_activities.max():.1f}")
    
    # Analyze key regions
    print("\n" + "=" * 78)
    print("SPECTRAL REGION ANALYSIS")
    print("=" * 78)
    
    regions = {
        'PO₂⁻ stretch': (980, 1100),
        'C-C lipid': (1060, 1130),
        'CH₂ scissoring': (1420, 1460),
        'Amide II': (1540, 1580),
        'Amide I': (1640, 1680)
    }
    
    for name, (low, high) in regions.items():
        mask = (frequencies >= low) & (frequencies <= high)
        n_peaks = mask.sum()
        if n_peaks > 0:
            max_int = raman_activities[mask].max()
            peak_freq = frequencies[mask][raman_activities[mask].argmax()]
            print(f"✓ {name:20s} ({low:4d}-{high:4d} cm⁻¹): {n_peaks:2d} peaks, strongest at {peak_freq:.1f} cm⁻¹")
        else:
            print(f"⚠ {name:20s} ({low:4d}-{high:4d} cm⁻¹): NO PEAKS")
    
    # Find top 10 peaks
    print("\n" + "=" * 78)
    print("TOP 10 RAMAN PEAKS")
    print("=" * 78)
    print(f"{'Rank':<6} {'Frequency (cm⁻¹)':<20} {'Raman Activity':<20}")
    print("-" * 78)
    
    top_indices = np.argsort(raman_activities)[-10:][::-1]
    for rank, idx in enumerate(top_indices, 1):
        print(f"{rank:<6} {frequencies[idx]:<20.2f} {raman_activities[idx]:<20.2f}")
    
    print("\n" + "=" * 78)
    print("✅ FREQUENCY CALCULATION SUCCESSFUL")
    print("   → Proceed to plot spectrum")
    print("=" * 78)
    
    return True, frequencies, raman_activities

def save_raman_data(frequencies, raman_activities, filename='raman_data.txt'):
    """Save extracted Raman data for plotting"""
    with open(filename, 'w') as f:
        f.write("# Raman spectrum data extracted from Gaussian\n")
        f.write("# Frequency (cm-1)    Raman Activity\n")
        for freq, activity in zip(frequencies, raman_activities):
            f.write(f"{freq:10.2f}    {activity:10.4f}\n")
    
    print(f"\n✓ Saved Raman data to: {filename}")
    print("  Use this with plot_raman_spectrum.py")
    
    # Also save Python arrays for easy copy-paste
    with open('raman_arrays.py', 'w') as f:
        f.write("# Copy these arrays into plot_raman_spectrum.py\n\n")
        f.write("freq = np.array([\n")
        for i in range(0, len(frequencies), 5):
            chunk = frequencies[i:i+5]
            f.write("    " + ", ".join(f"{x:.2f}" for x in chunk) + ",\n")
        f.write("])\n\n")
        
        f.write("raman_activ = np.array([\n")
        for i in range(0, len(raman_activities), 5):
            chunk = raman_activities[i:i+5]
            f.write("    " + ", ".join(f"{x:.2f}" for x in chunk) + ",\n")
        f.write("])\n")
    
    print(f"✓ Saved Python arrays to: raman_arrays.py")

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python validate_gaussian_output.py lipidA_opt.log")
        print("  python validate_gaussian_output.py lipidA_freq.log")
        sys.exit(1)
    
    logfile = sys.argv[1]
    
    # Determine job type from filename
    if 'opt' in logfile.lower():
        success = check_optimization_log(logfile)
    elif 'freq' in logfile.lower():
        success, frequencies, raman_activities = check_frequency_log(logfile)
        if success and frequencies is not None:
            save_raman_data(frequencies, raman_activities)
    else:
        # Try to auto-detect
        try:
            with open(logfile, 'r') as f:
                content = f.read()
            
            if 'Raman Activ' in content:
                print("Detected: Frequency calculation\n")
                success, frequencies, raman_activities = check_frequency_log(logfile)
                if success and frequencies is not None:
                    save_raman_data(frequencies, raman_activities)
            else:
                print("Detected: Optimization calculation\n")
                success = check_optimization_log(logfile)
        except:
            print("ERROR: Could not determine job type")
            sys.exit(1)
