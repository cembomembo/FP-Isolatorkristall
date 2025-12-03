import numpy as np
import matplotlib.pyplot as plt

def load_spectrum(filename):
    """
    Loads a Ba11/ISO .dat file.
    Returns (wavelength, voltage) as numpy arrays.
    """
    print(f"Loading {filename}...")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # Read metadata headers (comma to dot conversion handled)
            header1 = f.readline().strip().replace(",", ".") # Start WL
            header2 = f.readline().strip().replace(",", ".") # Gear factor
            header3 = f.readline().strip().replace(",", ".") # Direction

            # Read the numerical data
            data = np.loadtxt((line.replace(",", ".") for line in f), ndmin=2)

        start_wl = float(header1)
        gear = float(header2)
        direction = float(header3)

        t = data[:, 0]
        voltage = data[:, 1]

        wavelength = start_wl + (direction * gear * t)

        # Ensure wavelength always goes from Low -> High
        if wavelength[0] > wavelength[-1]:
            wavelength = wavelength[::-1]
            voltage = voltage[::-1]

        return wavelength, voltage

    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return np.array([]), np.array([])

# ==========================================
# Analysis for Task i
# ==========================================

file_xenon = "13Uhr26_FP_Ba11_Xenon_50mV.dat"
file_ruby = "13Uhr36_FP_Ba11_Ruby_50mV.dat"

wl_xe, int_xe = load_spectrum(file_xenon)
wl_ru, int_ru = load_spectrum(file_ruby)

if len(wl_xe) > 0 and len(wl_ru) > 0:

    calibration_offset = -4.57 
    wl_xe += calibration_offset
    wl_ru += calibration_offset

    wl_common = np.linspace(350, 720, 2000) 
    
    # Map the raw data onto this common grid
    int_xe_interp = np.interp(wl_common, wl_xe, int_xe)
    int_ru_interp = np.interp(wl_common, wl_ru, int_ru)

    int_xe_positive = -int_xe_interp

    absorption_spectrum = int_xe_positive - int_ru_interp

    plt.figure(figsize=(10, 6), dpi=150)
    plt.plot(wl_common, absorption_spectrum, color='green', label='Calculated Absorption ($I_{Xe} - I_{Ruby}$)')
    
    plt.plot(wl_common, int_xe_positive, color='orange', alpha=0.3, label='Xenon Emission (Source)')
    plt.plot(wl_common, int_ru_interp, color='red', alpha=0.3, label='Ruby Transmission')

    plt.title("Ruby Absorption Spectrum (Corrected)\nTask i: 350-720 nm")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity (V)")
    plt.xlim(350, 720)
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.text(410, max(absorption_spectrum)*0.8, "U-Band\n(Blue/Violet)", color='blue', ha='center')
    plt.text(560, max(absorption_spectrum)*0.8, "Y-Band\n(Green/Yellow)", color='green', ha='center')

    plt.tight_layout()
    plt.show()

else:
    print("Could not generate plot due to missing files.")