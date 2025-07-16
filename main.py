import os
from scripts.preprocess import preprocess_images
from scripts.breakup import analyze_breakup
from scripts.droplets import analyze_droplets
from scripts.empirical import compare_with_correlation

def get_int(msg): return int(input(msg).strip())
def get_float(msg): return float(input(msg).strip())
def get_tuple(msg, n, typ=float):
    vals = input(msg).strip().split(',')
    if len(vals) != n:
        raise ValueError(f"Expected {n} comma-separated values.")
    return tuple(typ(v.strip()) for v in vals)

def main():
    print("---- STAGE 1: PREPROCESSING ----")
    raw_dir = input('Path to RAW images: ').strip()
    flats_dir = input('Path to FLATFIELD images: ').strip()
    out_dir = input('Output directory: ').strip()
    n_imgs = get_int('Number of images to process: ')
    preprocess_images(raw_dir, flats_dir, out_dir, n_imgs)

    print("\n---- STAGE 2: BREAKUP LENGTH ----")
    px_per_mm_bl = get_float('Pixels per mm (breakup length): ')
    min_area_bl = get_float('Min contour area (px) for breakup detection: ')
    flip_bl = input('Flip image vertically for breakup detection? (yes/no): ').strip().lower() == "yes"
    analyze_breakup(
        os.path.join(out_dir, 'grayscale'),
        os.path.join(out_dir, 'breakup.csv'),
        px_per_mm_bl,
        min_area_bl,
        flip_bl
    )

    print("\n---- STAGE 3: DROPLET SIZE ANALYSIS ----")
    crop_box = get_tuple('🔲 Crop box (x1,y1,x2,y2): ', 4, int)
    min_area_dr = get_float('Min droplet area (px): ')
    max_area_dr = get_float('Max droplet area (px): ')
    t1 = get_int('First threshold for droplet detection (e.g. 100): ')
    t2 = get_int('Second threshold for droplet detection (e.g. 150): ')
    px_per_mm_dr = get_float('Pixels per mm (droplets): ')
    analyze_droplets(
        os.path.join(out_dir, 'grayscale'),
        os.path.join(out_dir, 'size_distributions'),
        crop_box, (t1, t2), min_area_dr, max_area_dr, px_per_mm_dr
    )

    print("\n---- STAGE 4: EMPIRICAL COMPARISON ----")
    fluid = input("Fluid name (e.g., sodium/water): ")
    pressure = get_float("Operating pressure (bar): ")
    Lb = get_float("Measured breakup length (mm): ")
    SMD = get_float("Measured SMD (mm): ")
    density = get_float("Fluid density (kg/m^3): ")
    viscosity = get_float("Fluid viscosity (Pa·s): ")
    surf_tens = get_float("Surface tension (N/m): ")
    compare_with_correlations(Lb, SMD, density, viscosity, surf_tens, pressure, fluid)

    print('\n Pre-processing complete!')

if __name__ == "__main__":
    main()

