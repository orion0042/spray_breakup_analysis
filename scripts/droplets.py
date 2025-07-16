import os, csv
import cv2
import numpy as np

def analyze_droplets(grayscale_dir, output_dir, crop, thresholds, min_area, max_area, px_per_mm):
    os.makedirs(output_dir, exist_ok=True)
    diameters = []
    mask_dir = os.path.join(output_dir, 'masks')
    os.makedirs(mask_dir, exist_ok=True)
    for fname in sorted(os.listdir(grayscale_dir)):
        img = cv2.imread(os.path.join(grayscale_dir, fname), cv2.IMREAD_GRAYSCALE)
        x1,y1,x2,y2 = crop
        roi = img[y1:y2, x1:x2]
        # Mask using both thresholds
        _, mask1 = cv2.threshold(roi, thresholds[0], 255, cv2.THRESH_BINARY_INV)
        _, mask2 = cv2.threshold(roi, thresholds[1], 255, cv2.THRESH_BINARY_INV)
        mask = cv2.bitwise_or(mask1, mask2)
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv2.contourArea(c)
            if min_area <= area <= max_area:
                diameter = 2 * np.sqrt(area/np.pi) / px_per_mm  # mm
                diameters.append(diameter)
        cv2.imwrite(os.path.join(mask_dir, fname), mask)
    # Save distributions
    with open(os.path.join(output_dir,"distribution.csv"), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Droplet diameter (mm)'])
        for d in diameters:
            writer.writerow([f"{d:.4f}"])
    print(f"Saved droplet mask images and {len(diameters)} diameters.")


