import os
import cv2
import csv

def analyze_breakup(gray_dir, output_csv, px_per_mm, min_area, flip):
    results = []
    for fname in sorted(os.listdir(gray_dir)):
        img = cv2.imread(os.path.join(gray_dir, fname), cv2.IMREAD_GRAYSCALE)
        if flip: img = cv2.flip(img, 0)
        _, binary = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)
        cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c) >= min_area:
                bx = cv2.boundingRect(c)
                breakup_px = bx[1] + bx[3]    # y + height
                breakup_mm = breakup_px / px_per_mm
                results.append([fname, breakup_mm])
                break
        else:
            results.append([fname, None])
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['image', 'breakup_length_mm'])
        writer.writerows(results)
