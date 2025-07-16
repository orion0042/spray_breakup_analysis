import cv2, os

def preprocess_images(raw_dir, flat_dir, out_dir, num_images):
    gray_dir = os.path.join(out_dir, 'grayscale')
    anno_dir = os.path.join(out_dir, 'annotated')
    flatcor_dir = os.path.join(out_dir, 'flat_corrected')
    os.makedirs(gray_dir, exist_ok=True)
    os.makedirs(anno_dir, exist_ok=True)
    os.makedirs(flatcor_dir, exist_ok=True)

    raws = sorted(os.listdir(raw_dir))[:num_images]
    flats = sorted(os.listdir(flat_dir))

    for i, fname in enumerate(raws):
        im = cv2.imread(os.path.join(raw_dir, fname), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # Flatfield correction if exists
        if i < len(flats):
            flat = cv2.imread(os.path.join(flat_dir, flats[i]), cv2.IMREAD_GRAYSCALE)
            flat = cv2.normalize(flat.astype('float32'), None, 0, 255, cv2.NORM_MINMAX)
            corrected = cv2.divide(gray.astype('float32'), flat + 1e-5)
            gray = cv2.normalize(corrected, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
            cv2.imwrite(os.path.join(flatcor_dir, f"corrected_{i:03d}.png"), gray)
        cv2.imwrite(os.path.join(gray_dir, f"gray_{i:03d}.png"), gray)
        annotated = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.putText(annotated, f"Frame {i}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imwrite(os.path.join(anno_dir, f"annotated_{i:03d}.png"), annotated)
    # Remove intermediate flat_corrected dir
    import shutil
    shutil.rmtree(flatcor_dir)

