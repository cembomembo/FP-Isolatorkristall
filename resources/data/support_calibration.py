import numpy as np

# --- Known Hg reference wavelengths (nm) ---
hg_ref = np.array([365.0, 404.7, 435.8, 546.1, 577.0, 579.0])

# --- Approximate peak positions seen by eye in the spectrum ---
initial_guesses = np.array([369, 409, 440, 551, 583, 585])

# --- The only file this calibration will use ---
hg_filename = "/home/lium/FP/ISO/FP-Isolatorkristall/resources/data/15Uhr03_FP_Ba11_Hg_Spectrum_50mV.dat"  # "15Uhr03_FP_Ba11_Hg_Spectrum_50mV.dat"


def load_hg_spectrum():
    """Load the fixed mercury calibration file and return (wavelength, intensity)."""
    with open(hg_filename, "r", encoding="utf-8") as f:
        start = float(f.readline().replace(",", "."))
        gear = float(f.readline().replace(",", "."))
        direction = float(f.readline().replace(",", "."))

        data = np.loadtxt((line.replace(",", ".") for line in f))

    t = data[:, 0]
    I_raw = data[:, 1]

    # Wavelength axis
    wl = start + direction * gear * t

    # Flip sign so peaks go upward
    I = -I_raw

    # Ensure ascending wavelength order
    if wl[0] > wl[-1]:
        wl = wl[::-1]
        I = I[::-1]

    return wl, I


def refine_peak(wl, I, guess, window=3):
    """Refine peak position by taking the maximum within ±window nm of a guessed location."""
    mask = (wl >= guess - window) & (wl <= guess + window)
    wl_win = wl[mask]
    I_win = I[mask]

    idx = np.argmax(I_win)
    return wl_win[idx]


def perform_hg_calibration():
    """
    Finds the exact measured Hg peak wavelengths and computes the wavelength offset Δλ.
    """
    wl, I = load_hg_spectrum()

    # refine all 6 peaks
    measured = np.array([refine_peak(wl, I, g) for g in initial_guesses])

    # compute shifts
    shifts = hg_ref - measured
    shift_mean = shifts.mean()

    print("Reference Hg lines (nm):", hg_ref)
    print("Measured Hg peaks (nm): ", measured)
    print("Individual shifts (nm):", shifts)
    print(f"\nMean wavelength shift Δλ = {shift_mean:.3f} nm")

    return shift_mean, measured, wl, I


# --- Run calibration immediately ---
shift, measured_peaks, wl_hg, I_hg = perform_hg_calibration()


def apply_calibration(wavelength, shift=shift):
    """Apply Δλ shift to any wavelength axis."""
    return np.asarray(wavelength) + shift
