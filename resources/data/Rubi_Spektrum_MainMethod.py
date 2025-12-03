import numpy as np
import matplotlib.pyplot as plt

def load_spectrum(filename):
    """Loads a .dat file without altering data."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            header1 = f.readline().strip().replace(",", ".")
            header2 = f.readline().strip().replace(",", ".")
            header3 = f.readline().strip().replace(",", ".")
            data = np.loadtxt((line.replace(",", ".") for line in f), ndmin=2)
        
        start_wl = float(header1)
        gear = float(header2)
        direction = float(header3)
        t = data[:, 0]
        voltage = data[:, 1]
        
        wavelength = start_wl + (direction * gear * t)
        
        # Sort wavelength low -> high
        if wavelength[0] > wavelength[-1]:
            wavelength = wavelength[::-1]
            voltage = voltage[::-1]
            
        return wavelength, voltage
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return np.array([]), np.array([])

# 1. Define filenames for the "Intended Method"
# We compare the Ruby measurement against the empty machine Baseline.
file_diff = "13Uhr15_FP_Ba11_Difference_50mV.dat"  # Ruby in Probe arm
file_base = "14Uhr29_FP_Ba11_Baseline_50mV.dat"    # Pinhole in Probe arm

# 2. Load Data
wl_diff, int_diff = load_spectrum(file_diff)
wl_base, int_base = load_spectrum(file_base)

if len(wl_diff) > 0 and len(wl_base) > 0:
    # 3. Apply Calibration (Task h)
    cal_offset = -4.57
    wl_diff += cal_offset
    wl_base += cal_offset
    
    # 4. Interpolate to common grid
    wl_common = np.linspace(350, 720, 2000)
    diff_interp = np.interp(wl_common, wl_diff, int_diff)
    base_interp = np.interp(wl_common, wl_base, int_base)
    
    # 5. The Intended Calculation
    # Theory: Difference = (Ruby - Ref). Baseline = (Empty - Ref).
    # Subtracting them: (Ruby - Ref) - (Empty - Ref) = Ruby - Empty.
    # Since Ruby absorbs, "Ruby" is smaller than "Empty", so the result is negative.
    # To see POSITIVE absorption peaks, we usually calculate: Baseline - Difference.
    intended_result = base_interp - diff_interp
    
    # 6. Plotting
    plt.figure(figsize=(10, 6), dpi=150)
    
    plt.plot(wl_common, intended_result, color='purple', label='Intended Method (Baseline - Difference)')
    plt.plot(wl_common, base_interp, color='gray', linestyle='--', alpha=0.5, label='Baseline (Should be 0)')
    plt.plot(wl_common, diff_interp, color='blue', alpha=0.3, label='Raw Difference (Ruby)')

    plt.axhline(0, color='black', linewidth=0.8)
    plt.title("Verification of Intended Method\n(Baseline Subtraction)")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity (V)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.show()
else:
    print("Files missing.")