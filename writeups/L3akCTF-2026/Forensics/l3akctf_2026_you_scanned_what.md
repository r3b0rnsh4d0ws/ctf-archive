# You Scanned WHAT?!? — L3akCTF 2026 Forensics

## Challenge
- **CTF**: L3akCTF 2026
- **Category**: Forensics
- **Author**: JAGIC
- **Flag**: `L3AK{X-r4Y_C0mp1373!}`

## Files
- `scan.7z` — Password-free archive containing `scan.sqlite`
- `scan.sqlite` — SQLite database with a single table `projections` (180 rows, one per angle 0°–179°)
  - Columns: `angle_degrees` (INTEGER PK), `detector_count` (INTEGER), `light_values` (TEXT — Python list of floats)

## Recon
Each row represents a **1D X-ray projection** at a given angle — i.e. a CT (computed tomography) sinogram row. The `light_values` contain transmission intensity readings across a detector array. The `detector_count` varies (215–543) because each projection was cropped to its non-empty detector range.

## Analysis
1. **Parse** each projection's `light_values` (Python list literal) into numpy arrays
2. **Build sinogram** (180×543) by center-padding each projection to the max detector count
3. **Filtered back-projection** — the standard CT reconstruction algorithm:
   - Apply Ram-Lak ramp filter in frequency domain (`|f|` filter via FFT)
   - Back-project each filtered projection onto the 2D image grid with linear interpolation
4. The raw sinogram values are already well-scaled (intensity ~18–166), so no Beer-Lambert normalization was needed

## Exploit
```python
# Core reconstruction (simplified)
sinogram = build_sinogram(projections)       # shape (180, 543)
filtered = ramp_filter(sinogram)             # Ram-Lak |f| filter via FFT
image = vectorized_backproject(filtered)     # Linear interpolation back-projection
```
Best result: **filtered back-projection on raw (unnormalized) sinogram** — produces sharp, readable text and the mascot image.

## Flag
```
L3AK{X-r4Y_C0mp1373!}
```

## Lessons
- CT scan data is just a sinogram: 1D projections at many angles, stored in a database
- Variable detector counts mean projections were cropped to non-empty regions — center-padding recovers the full field of view
- **Filtered back-projection** (ramp filter + BP) produces far sharper results than simple unfiltered BP
- Values in the sinogram were "light" (transmission) but already at the right scale for reconstruction — no Beer-Lambert needed
- The author likely used Python + `scipy.ndimage.radon`/`iradon` (or a custom implementation) to generate the sinogram from a source image (the L3akCTF mascot + flag text)
