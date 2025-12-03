import numpy as np
import matplotlib.pyplot as plt

def load_and_sort_spectrum(filename):
    """
    Loads a .dat file.
    CRITICAL: Uses the direction header (+1 or -1) to calculate wavelength,
    then sorts arrays so wavelength is always increasing (Low -> High).
    """
    print(f"Loading {filename}...")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            header1 = f.readline().strip().replace(",", ".")
            header2 = f.readline().strip().replace(",", ".")
            header3 = f.readline().strip().replace(",", ".")
            data = np.loadtxt((line.replace(",", ".") for line in f), ndmin=2)
        
        start_wl = float(header1)
        gear = float(header2)
        direction = float(header3) # +1 (Up) or -1 (Down)

        t = data[:, 0]
        voltage = data[:, 1]
        
        # 1. Calculate Wavelength based on scan direction
        wavelength = start_wl + (direction * gear * t)
        
        # 2. Sort Data (Low Wavelength -> High Wavelength)
        # This fixes the "Jagged Slope" error if one file was Up and the other Down.
        sort_indices = np.argsort(wavelength)
        sorted_wl = wavelength[sort_indices]
        sorted_vol = voltage[sort_indices]
            
        return sorted_wl, sorted_vol

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return np.array([]), np.array([])

# ==========================================
# Task l: High Sensitivity Analysis (R-Lines)
# ==========================================

# 1. Define the 5mV Files (High Sensitivity)
# [cite_start]According to handwritten notes [cite: 684-688]:
# Xenon was scanned DOWN. Ruby was likely scanned DOWN. 
# Our loader handles this automatically.
file_xe_high = "13Uhr57_FP_Ba11_Xenon_5mV.dat"
file_ru_high = "14Uhr10_FP_Ba11_Ruby_5mV.dat"

wl_xe, int_xe = load_and_sort_spectrum(file_xe_high)
wl_ru, int_ru = load_and_sort_spectrum(file_ru_high)

if len(wl_xe) > 0 and len(wl_ru) > 0:
    
    # 2. Apply Calibration (Result from Task h)
    cal_offset = -4.57
    wl_xe += cal_offset
    wl_ru += cal_offset

    # 3. Fix Signs
    # Xenon (Ref beam) is recorded as negative. Flip to Positive.
    # Ruby (Probe beam) is recorded as positive. Keep it.
    int_xe = -int_xe 

    # 4. Interpolate to Common Grid
    # Create a grid focused strictly on the Red region
    wl_common = np.linspace(670, 720, 1000)
    
    int_xe_interp = np.interp(wl_common, wl_xe, int_xe)
    int_ru_interp = np.interp(wl_common, wl_ru, int_ru)

    # 5. Calculate Absorption
    # Absorption = Source (Xe) - Transmitted (Ru)
    absorption_high_sens = int_xe_interp - int_ru_interp

    # 6. Plotting
    plt.figure(figsize=(10, 6), dpi=150)
    
    # Plot the calculated absorption
    plt.plot(wl_common, -absorption_high_sens, color='darkred', linewidth=1.2, label='Absorption ($I_{Xe} - I_{Ru}$)')
    
    # Add Marker for R-Lines (Theoretical Position)
    plt.axvline(x=694, color='coral', linestyle='--', alpha=0.6, label='R1-Line (694.0 nm)')

    plt.axvline(x=692.5, color='violet', linestyle='--', alpha=0.6, label='R2-Line (692.5 nm)')

    # Formatting
    plt.title("High-Sensitivity Measurement of Forbidden Transitions")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Absorption Intensity (V)")
    plt.xlim(670, 720)
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("../figures/RLines_Spectrum.png") # Save this to replace Figure 14
    plt.show()

else:
    print("Could not generate plot. Check filenames.")