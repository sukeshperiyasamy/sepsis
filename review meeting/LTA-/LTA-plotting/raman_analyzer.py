"""
Raman Spectrum Analysis Script
===============================
This script analyzes Raman spectroscopy data from Excel files.

Author: Auto-generated
Date: March 7, 2026

Features:
- Automatic column detection
- Data cleaning and validation
- Savitzky-Golay smoothing
- Peak detection with scipy
- Excel output of detected peaks
- Visualization with matplotlib
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
import os


class RamanAnalyzer:
    """
    A class to analyze Raman spectroscopy data.
    
    Attributes:
        file_path (str): Path to the Excel file containing Raman data
        data (pd.DataFrame): Raw data from Excel file
        raman_shift (np.array): Cleaned Raman shift values
        intensity (np.array): Cleaned intensity values
        smoothed_intensity (np.array): Smoothed intensity values
        peaks (dict): Detected peak information
    """
    
    def __init__(self, file_path):
        """
        Initialize the RamanAnalyzer with an Excel file path.
        
        Parameters:
            file_path (str): Path to the Excel file
        """
        self.file_path = file_path
        self.data = None
        self.raman_shift = None
        self.intensity = None
        self.smoothed_intensity = None
        self.peaks = None
        
    def load_data(self):
        """
        Load data from Excel file and automatically detect columns.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Loading data from: {self.file_path}")
            # Read Excel file
            self.data = pd.read_excel(self.file_path)
            
            # Automatically detect columns (assumes 2 columns: Raman shift and Intensity)
            if self.data.shape[1] >= 2:
                print(f"Detected {self.data.shape[1]} columns")
                print(f"Column names: {list(self.data.columns)}")
                
                # Use first two columns
                col1, col2 = self.data.columns[0], self.data.columns[1]
                print(f"Using columns: '{col1}' and '{col2}'")
                
                self.raman_shift = self.data.iloc[:, 0].values
                self.intensity = self.data.iloc[:, 1].values
                
                print(f"Loaded {len(self.raman_shift)} data points")
                return True
            else:
                print("Error: Excel file must contain at least 2 columns")
                return False
                
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def clean_data(self):
        """
        Clean the data by removing NaN values, ensuring numeric data, and sorting.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("\nCleaning data...")
            
            # Create a DataFrame for easier cleaning
            df = pd.DataFrame({
                'raman_shift': self.raman_shift,
                'intensity': self.intensity
            })
            
            # Remove NaN values
            initial_size = len(df)
            df = df.dropna()
            removed = initial_size - len(df)
            if removed > 0:
                print(f"Removed {removed} rows with NaN values")
            
            # Convert to numeric (coerce errors to NaN, then drop)
            df['raman_shift'] = pd.to_numeric(df['raman_shift'], errors='coerce')
            df['intensity'] = pd.to_numeric(df['intensity'], errors='coerce')
            df = df.dropna()
            
            # Sort by Raman shift
            df = df.sort_values('raman_shift')
            df = df.reset_index(drop=True)
            
            # Update arrays
            self.raman_shift = df['raman_shift'].values
            self.intensity = df['intensity'].values
            
            print(f"Data cleaned. Final size: {len(df)} points")
            print(f"Raman shift range: {self.raman_shift.min():.1f} - {self.raman_shift.max():.1f} cm^-1")
            print(f"Intensity range: {self.intensity.min():.2f} - {self.intensity.max():.2f}")
            
            return True
            
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return False
    
    def smooth_spectrum(self, window_length=11, polyorder=3):
        """
        Smooth the spectrum using Savitzky-Golay filter.
        
        Parameters:
            window_length (int): Length of the filter window (must be odd)
            polyorder (int): Order of the polynomial used to fit the samples
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"\nSmoothing spectrum (window={window_length}, polyorder={polyorder})...")
            
            # Ensure window_length is odd
            if window_length % 2 == 0:
                window_length += 1
            
            # Apply Savitzky-Golay filter
            self.smoothed_intensity = savgol_filter(
                self.intensity, 
                window_length=window_length, 
                polyorder=polyorder
            )
            
            print("Smoothing complete")
            return True
            
        except Exception as e:
            print(f"Error smoothing spectrum: {e}")
            return False
    
    def detect_peaks(self, prominence=2.0, height=5.0, distance=5):
        """
        Detect peaks in the smoothed spectrum.
        
        Parameters:
            prominence (float): Required prominence of peaks
            height (float): Minimum height of peaks
            distance (int): Minimum distance between peaks (in data points)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"\nDetecting peaks (prominence={prominence}, height={height}, distance={distance})...")
            
            # Use smoothed intensity if available, otherwise raw intensity
            intensity_to_use = self.smoothed_intensity if self.smoothed_intensity is not None else self.intensity
            
            # Detect peaks
            peak_indices, properties = find_peaks(
                intensity_to_use,
                prominence=prominence,
                height=height,
                distance=distance
            )
            
            # Store peak information
            self.peaks = {
                'indices': peak_indices,
                'raman_shift': self.raman_shift[peak_indices],
                'intensity': intensity_to_use[peak_indices],
                'properties': properties
            }
            
            print(f"Detected {len(peak_indices)} peaks")
            
            return True
            
        except Exception as e:
            print(f"Error detecting peaks: {e}")
            return False
    
    def print_peak_table(self):
        """
        Print a formatted table of detected peaks.
        """
        if self.peaks is None:
            print("No peaks detected yet. Run detect_peaks() first.")
            return
        
        print("\n" + "="*60)
        print("DETECTED PEAKS")
        print("="*60)
        
        # Create DataFrame for nice formatting
        peak_df = pd.DataFrame({
            'Raman Shift (cm^-1)': self.peaks['raman_shift'],
            'Intensity': self.peaks['intensity']
        })
        
        # Sort by intensity (descending)
        peak_df = peak_df.sort_values('Intensity', ascending=False)
        peak_df = peak_df.reset_index(drop=True)
        peak_df.index = peak_df.index + 1  # Start counting from 1
        
        print(peak_df.to_string())
        print("="*60)
        print(f"Total peaks: {len(peak_df)}\n")
    
    def save_peaks_to_excel(self, output_file='LTA_detected_peaks.xlsx'):
        """
        Save detected peaks to an Excel file.
        
        Parameters:
            output_file (str): Name of the output Excel file
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.peaks is None:
            print("No peaks detected yet. Run detect_peaks() first.")
            return False
        
        try:
            # Create DataFrame
            peak_df = pd.DataFrame({
                'Raman Shift (cm^-1)': self.peaks['raman_shift'],
                'Intensity': self.peaks['intensity']
            })
            
            # Sort by Raman shift
            peak_df = peak_df.sort_values('Raman Shift (cm^-1)')
            peak_df = peak_df.reset_index(drop=True)
            
            # Get output path (same directory as input file)
            output_dir = os.path.dirname(self.file_path)
            output_path = os.path.join(output_dir, output_file)
            
            # Save to Excel
            peak_df.to_excel(output_path, index=False)
            
            print(f"[OK] Peaks saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving peaks to Excel: {e}")
            return False
    
    def plot_spectrum(self, save_file='LTA_raman_analysis.png', dpi=300, figsize=(14, 10)):
        """
        Plot raw and smoothed Raman spectra with detected peaks.
        
        Parameters:
            save_file (str): Name of the output image file
            dpi (int): Resolution of the saved image
            figsize (tuple): Figure size (width, height) in inches
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"\nGenerating plots...")
            
            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
            
            # Plot 1: Raw Raman Spectrum
            ax1.plot(self.raman_shift, self.intensity, 'b-', linewidth=1.5, label='Raw spectrum')
            ax1.set_xlabel('Raman Shift (cm$^{-1}$)', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Intensity (a.u.)', fontsize=12, fontweight='bold')
            ax1.set_title('Raw Raman Spectrum', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3, linestyle='--')
            ax1.legend(loc='upper right', fontsize=10)
            
            # Invert x-axis (standard Raman convention)
            ax1.invert_xaxis()
            
            # Plot 2: Smoothed Raman Spectrum with Peaks
            if self.smoothed_intensity is not None:
                ax2.plot(self.raman_shift, self.smoothed_intensity, 'b-', 
                        linewidth=2, label='Smoothed spectrum')
                
                # Mark detected peaks
                if self.peaks is not None:
                    ax2.plot(self.peaks['raman_shift'], self.peaks['intensity'], 
                            'r^', markersize=8, label=f"Detected peaks ({len(self.peaks['raman_shift'])})")
                    
                    # Annotate top 5 peaks
                    peak_df = pd.DataFrame({
                        'shift': self.peaks['raman_shift'],
                        'intensity': self.peaks['intensity']
                    }).sort_values('intensity', ascending=False)
                    
                    for i in range(min(5, len(peak_df))):
                        shift = peak_df.iloc[i]['shift']
                        intensity = peak_df.iloc[i]['intensity']
                        ax2.annotate(f'{shift:.0f}', 
                                   xy=(shift, intensity), 
                                   xytext=(0, 10),
                                   textcoords='offset points',
                                   ha='center',
                                   fontsize=9,
                                   bbox=dict(boxstyle='round,pad=0.3', 
                                           facecolor='yellow', 
                                           alpha=0.7))
            
            ax2.set_xlabel('Raman Shift (cm$^{-1}$)', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Intensity (a.u.)', fontsize=12, fontweight='bold')
            ax2.set_title('Smoothed Raman Spectrum with Detected Peaks', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3, linestyle='--')
            ax2.legend(loc='upper right', fontsize=10)
            
            # Invert x-axis
            ax2.invert_xaxis()
            
            # Adjust layout
            plt.tight_layout()
            
            # Save figure
            output_dir = os.path.dirname(self.file_path)
            output_path = os.path.join(output_dir, save_file)
            plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
            
            print(f"[OK] Plot saved to: {output_path}")
            
            # Show plot
            plt.show()
            
            return True
            
        except Exception as e:
            print(f"Error plotting spectrum: {e}")
            return False


def main():
    """
    Main function to run the Raman spectrum analysis pipeline.
    """
    # Configuration
    FILE_PATH = r"C:\Users\sukes\Downloads\LTA-\LTA-plotting\LTA-sim-data.xlsx"
    
    # Peak detection parameters (adjustable)
    PEAK_PROMINENCE = 2.0  # Minimum prominence of peaks
    PEAK_HEIGHT = 5.0      # Minimum height of peaks
    PEAK_DISTANCE = 5      # Minimum distance between peaks (data points)
    
    # Smoothing parameters (adjustable)
    SMOOTH_WINDOW = 11     # Window length for Savitzky-Golay filter (must be odd)
    SMOOTH_POLYORDER = 3   # Polynomial order for smoothing
    
    print("="*70)
    print("RAMAN SPECTRUM ANALYSIS")
    print("="*70)
    
    # Create analyzer instance
    analyzer = RamanAnalyzer(FILE_PATH)
    
    # Step 1: Load data
    if not analyzer.load_data():
        print("Failed to load data. Exiting.")
        return
    
    # Step 2: Clean data
    if not analyzer.clean_data():
        print("Failed to clean data. Exiting.")
        return
    
    # Step 3: Smooth spectrum
    if not analyzer.smooth_spectrum(window_length=SMOOTH_WINDOW, polyorder=SMOOTH_POLYORDER):
        print("Failed to smooth spectrum. Exiting.")
        return
    
    # Step 4: Detect peaks
    if not analyzer.detect_peaks(prominence=PEAK_PROMINENCE, height=PEAK_HEIGHT, distance=PEAK_DISTANCE):
        print("Failed to detect peaks. Exiting.")
        return
    
    # Step 5: Print peak table
    analyzer.print_peak_table()
    
    # Step 6: Save peaks to Excel
    analyzer.save_peaks_to_excel('LTA_detected_peaks.xlsx')
    
    # Step 7: Plot and save visualization
    analyzer.plot_spectrum('LTA_raman_analysis.png', dpi=300)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nOutput files:")
    print("  1. LTA_detected_peaks.xlsx - Detected peak data")
    print("  2. LTA_raman_analysis.png  - Visualization plots")
    print("\nTo modify parameters, edit the configuration section in main()")


if __name__ == "__main__":
    main()
