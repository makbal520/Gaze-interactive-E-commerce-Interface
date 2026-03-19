## Shopping Gaze (Eye-tracking Interactive Ad) + Report

This repository contains:

1. A gaze-responsive shopping demo webpage (WebGazer-based)
2. Python scripts to generate gaze heatmaps and bag-area fixation visualizations
3. The final written report PDFs

> Note: `Data and seperate analysis/` is excluded from GitHub via `.gitignore` (it is intentionally not uploaded).

---

## Repository Structure

- `Webpage/`
  - `final_no_neg.html`: demo page (no negative-feedback condition)
  - `final_with_neg.html`: demo page (with negative-feedback condition)
  - Media files used by the pages (images/videos)

- `heatmap and fixation comparision analysis/`
  - `beautiful_bag_visualization.py`: generates “beautiful” bag-area visualizations using the HTML-defined bag-area region
  - `enhanced_group_heatmap.py`: generates enhanced group heatmaps + side-by-side comparison
  - Precomputed CSV inputs + generated PNG outputs used by the scripts

- `Final Report.pdf`, `Final presentation.pdf`, `Project documents.zip`

---

## Demo Webpages (View in Browser)

You can open the HTML files directly:

- `Webpage/final_no_neg.html`
- `Webpage/final_with_neg.html`

The pages use WebGazer from a CDN:
`https://webgazer.cs.brown.edu/webgazer.js`

### Recommended local running mode

For the best browser compatibility with camera/eye-tracking permissions, run a local static server and open the page via `http://localhost`:

```bash
cd "Webpage"
python3 -m http.server 8000
```

Then open:

- http://localhost:8000/final_no_neg.html
- http://localhost:8000/final_with_neg.html

During the demo:

- Click “Start Calibration”
- After calibration, watch the gaze-responsive advertisement behavior
- Use “Download Data” to export recorded data (CSV + JSON)

---

## Heatmaps & Bag-Area Fixation Visualizations

### Prerequisites

The Python scripts are written in Python 3 and rely on:

- `numpy`
- `matplotlib`
- `seaborn`
- `scipy`
- `Pillow`

Install (example):

```bash
pip install numpy matplotlib seaborn scipy pillow
```

### 1) Beautiful bag-area visualizations

From inside the heatmap folder:

```bash
cd "heatmap and fixation comparision analysis"
python3 beautiful_bag_visualization.py
```

It uses the bag-area region defined in the HTML (percent-based coordinates like `x=0.54`, `y=0.55`, `width=0.31`, `height=0.45`) and the included CSV files (e.g. `101_fixations.csv`, `101_gaze_data.csv`, etc.).

Expected generated outputs (PNG):

- `beautiful_multi_size_dashboard.png`
- `beautiful_focused_analysis.png`
- `beautiful_statistical_comparison.png`
- `beautiful_bag_location_visualization.png`
- `beautiful_duration_analysis.png`

### 2) Enhanced group heatmaps

```bash
cd "heatmap and fixation comparision analysis"
python3 enhanced_group_heatmap.py
```

Expected generated outputs (PNG):

- `enhanced_group1_heatmap.png`
- `enhanced_group2_heatmap.png`
- `enhanced_group_comparison.png`

---

## Final Materials

- `Final Report.pdf`: full written report
- `Final presentation.pdf`: slides/presentation
- `Project documents.zip`: additional project documents

---

## Data Exclusion / Reproducibility

The raw dataset and extended analysis work under `Data and seperate analysis/` are excluded from GitHub (see `.gitignore`).

However, the heatmap scripts in `heatmap and fixation comparision analysis/` include the required preprocessed CSV inputs needed to generate the included PNG visualizations.

