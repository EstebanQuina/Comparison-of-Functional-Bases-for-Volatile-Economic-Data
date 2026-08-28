# Comparison of Functional Bases for Volatile Economic Data

Undergraduate thesis (Yachay Tech University) comparing B-spline, Fourier, and
wavelet basis expansions for representing volatile Latin American GDP growth
trajectories, and evaluating how the choice of basis affects Functional
Principal Component Analysis (FPCA).

## Motivation

Functional Data Analysis (FDA) treats each country's growth trajectory as a
continuous function rather than a sequence of discrete observations, which
requires first expanding it in a basis system. Most applications to
macroeconomic series default to smooth, globally supported bases (B-splines,
Fourier), implicitly assuming bounded, uniformly distributed roughness.
Latin American GDP growth series violate that assumption: they are punctuated
by abrupt, localized shocks (the 1982 debt crisis, the 1999 regional currency
crises, the 2008 global financial crisis, the 2020 COVID-19 contraction) whose
timing and magnitude differ sharply across countries.

This thesis extends the dataset and approach of Padilla-Segarra et al. (2020)
to test whether wavelets — which localize simultaneously in time and
frequency and form an unconditional basis for Besov spaces — better preserve
crisis episodes than globally smooth bases, and how that choice propagates
into the interpretability of the resulting FPCA.

**General objective:** comparatively evaluate B-spline, Fourier, and wavelet
basis expansions for representing GDP growth trajectories of volatile Latin
American economies, in terms of reconstruction fidelity, coefficient economy,
and their effect on the interpretability of the resulting FPCA.

## Data

Annual GDP growth rates (percentage points) for 20 Latin American countries,
1960–2024, sourced from World Bank Open Data. Extends the original 1960–2018
panel of Padilla-Segarra et al. through 2024, adding the COVID-19 contraction
and the heterogeneous post-pandemic recovery. Missing values (1960 for most
countries; 1960–1965 for El Salvador; 1960–1971 for Cuba) are handled via
linear interpolation plus forward/backward fill, used only to construct the
functional representation — all reconstruction metrics are evaluated on
observed, non-imputed points only.

## Methods

Three basis families are compared under a common, reproducible pipeline:

- **B-spline** (baseline, replicating Padilla-Segarra et al.): smoothing
  spline with a per-country, data-driven smoothing parameter derived from a
  robust noise estimate of first differences.
- **Fourier**: truncated Discrete Fourier Transform at K ∈ {5, 10, 15}
  components; used to examine the Gibbs phenomenon near structural breaks.
- **Wavelet**: multi-level discrete wavelet transform (Haar, Daubechies-2,
  Symlet-4), implemented from scratch as an explicit orthogonal matrix with
  circular boundary conditions for exact round-trip reconstruction, denoised
  via soft thresholding.

Basis families are compared using three metrics: reconstruction error (RMSE
on observed points), coefficient sparsity (fraction of wavelet coefficients
zeroed at matched RMSE), and FPCA variance explained (number of components
needed to reach 80% cumulative variance). All analysis is implemented in
Python 3.12.

## Repository structure

```
.
├── DataCollection.ipynb          # World Bank data retrieval and panel construction
├── smoothing/                    # Core analysis pipeline
│   ├── latin_america_gdp_growth.csv
│   ├── 01_exploratory_analysis.py   # Trajectories, volatility, crisis heatmap
│   ├── 02_basis_expansions.py       # B-spline / Fourier / wavelet fitting
│   ├── 02b_wavelet_fix.py           # Corrected wavelet pipeline (matrix DWT, fair RMSE comparison)
│   ├── 03_fpca.py                   # FPCA replication/extension of Padilla-Segarra et al.
│   └── output/                      # Generated figures, organized by script
├── manuscript/
│   └── Yachay_Tech_University___Undergraduate_Thesis_Template/
│       ├── main.tex               # Thesis entry point (LaTeX, book class)
│       ├── main.pdf                # Compiled thesis
│       ├── chapters/               # introduction, methodology, results, etc.
│       ├── bib/                    # Bibliography
│       └── figures/, images/       # Manuscript assets
├── state_of_art/
│   └── protocolo_estado_del_arte.md # Literature review protocol
├── requirements.txt
└── setup_environment.sh
```

## Reproducing the analysis

```bash
bash setup_environment.sh        # creates fda_env/ and installs dependencies
source fda_env/bin/activate

python smoothing/01_exploratory_analysis.py
python smoothing/02_basis_expansions.py
python smoothing/02b_wavelet_fix.py
python smoothing/03_fpca.py
```

Each script reads `smoothing/latin_america_gdp_growth.csv` and writes its
figures to a corresponding subfolder of `smoothing/output/`. Dependencies are
also listed in `requirements.txt` for use with any Python 3.12 environment
manager.

## Manuscript

The full thesis (LaTeX source and compiled PDF) is in
[`manuscript/Yachay_Tech_University___Undergraduate_Thesis_Template/`](manuscript/Yachay_Tech_University___Undergraduate_Thesis_Template/),
built on Yachay Tech University's official undergraduate thesis template.

## Author

Esteban Quiña — Yachay Tech University
