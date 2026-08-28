# ============================================================
# Thesis: Comparative Analysis of Functional Bases for
#         Volatile Economic Series
# Script 03: Functional Principal Component Analysis (FPCA)
# Author: Esteban Quiña
# ============================================================
# This script replicates and extends Table 2 of Padilla-Segarra
# et al. (2020), comparing FPCA results across:
#   - Raw data (= B-spline interpolation, baseline)
#   - B-spline smoothing (adaptive sigma-based)
#   - Fourier basis (5, 10, 15 components)
#   - Wavelet Sym4 (at λ=0 and λ matched to B-spline RMSE)
#
# Key insight from diagnostic:
#   Raw data FPCA gives FPC1=21.3%, FPC2=15.9%, FPC3=10.0%,
#   3-FPC total=47.2% — replicating the original paper's 47.1%.
#   B-spline SMOOTHING collapses variance into FPC1 (98%+)
#   because it removes cross-country variation in volatility.
#   Wavelets with increasing λ progressively consolidate variance.
# ============================================================
# Run:  python smoothing/03_fpca.py
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import UnivariateSpline
from scipy.fft import fft, ifft
from pathlib import Path

# ── 0. Paths ──────────────────────────────────────────────────
DATA_PATH  = Path("smoothing/latin_america_gdp_growth.csv")
OUTPUT_DIR = Path("smoothing/output/03_fpca")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CRISIS_YEARS     = {1982: "Debt Crisis", 1999: "LatAm Crises",
                    2008: "GFC",         2020: "COVID-19"}
WAVELET_LEVELS   = 4
PALETTE          = plt.cm.tab20(np.linspace(0, 1, 20))

# ── 1. Load data ──────────────────────────────────────────────
df_raw    = pd.read_csv(DATA_PATH)
years     = list(range(1960, 2025))
countries = df_raw["economy"].tolist()
names     = dict(zip(df_raw["economy"], df_raw["Country"]))
short     = {c: names[c].replace(", RB","").replace(
                 "Dominican Republic","Dom. Rep.") for c in countries}

GDP = df_raw.set_index("economy").drop(columns="Country")
GDP.columns = [int(c.replace("YR", "")) for c in GDP.columns]
GDP = GDP[years]
t   = np.array(years, dtype=float)

print("=" * 65)
print("  Script 03: FPCA Comparison across Functional Bases")
print("=" * 65)

# ── 2. Helpers ────────────────────────────────────────────────
def fill_gaps(y):
    return pd.Series(y).interpolate('linear').ffill().bfill().values

# ── 3. Wavelet infrastructure ─────────────────────────────────
_db2_lo = np.array([
    (1+np.sqrt(3))/(4*np.sqrt(2)), (3+np.sqrt(3))/(4*np.sqrt(2)),
    (3-np.sqrt(3))/(4*np.sqrt(2)), (1-np.sqrt(3))/(4*np.sqrt(2))])

def _make_hi(lo):
    N = len(lo)
    return np.array([(-1)**k * lo[N-1-k] for k in range(N)])

_sym4_lo = np.array([
    -0.075765714789356680, -0.029635527645960390,
     0.497618667632562900,  0.803738751805914900,
     0.297857795605605050, -0.099219543576947200,
    -0.012603967262030850,  0.032223100604078150])

FILTERS = {
    'haar': {'lo': np.array([1.,1.])/np.sqrt(2),
             'hi': np.array([-1.,1.])/np.sqrt(2)},
    'db2':  {'lo': _db2_lo,  'hi': _make_hi(_db2_lo)},
    'sym4': {'lo': _sym4_lo, 'hi': _make_hi(_sym4_lo)},
}

def _build_W(n, lo, hi):
    f = len(lo); W = np.zeros((n, n))
    for i in range(n//2):
        for j in range(f):
            W[i, (2*i+j)%n] += lo[j]
            W[i+n//2, (2*i+j)%n] += hi[j]
    return W

def wavedec(y, wavelet='sym4', levels=4):
    lo, hi = FILTERS[wavelet]['lo'], FILTERS[wavelet]['hi']
    n_orig = len(y)
    n_pad  = int(2**np.ceil(np.log2(n_orig)))
    x      = np.resize(y.astype(float), n_pad)
    details, level_ns = [], []
    cur = x
    for _ in range(levels):
        n = len(cur); W = _build_W(n, lo, hi); out = W @ cur
        level_ns.append(n); details.append(out[n//2:]); cur = out[:n//2]
    return cur, details, level_ns, n_orig

def waverec(ap, details, level_ns, wavelet, n_orig):
    lo, hi = FILTERS[wavelet]['lo'], FILTERS[wavelet]['hi']
    cur = ap.copy()
    for det, n in zip(reversed(details), reversed(level_ns)):
        W = _build_W(n, lo, hi); cur = W.T @ np.concatenate([cur, det])
    return cur[:n_orig]

def soft_thr(details, lam):
    return [np.sign(d)*np.maximum(np.abs(d)-lam, 0) for d in details]

# ── 4. Build functional data matrices ─────────────────────────
def build_raw_matrix():
    """Gap-filled observed data — baseline (≈ interpolating B-spline)."""
    return np.array([fill_gaps(GDP.loc[c].values.astype(float))
                     for c in countries])

def build_bspline_matrix(smooth_factor=1.0):
    """B-spline smoothing with adaptive sigma."""
    X = np.zeros((len(countries), len(t)))
    for i, c in enumerate(countries):
        y = GDP.loc[c].values.astype(float)
        mask = ~np.isnan(y)
        t_obs, y_obs = t[mask], y[mask]
        diffs = np.diff(y_obs)
        sigma = np.median(np.abs(diffs-np.median(diffs)))/0.6745/np.sqrt(2)
        sigma = max(sigma, 0.1)
        spl   = UnivariateSpline(t_obs, y_obs, k=3,
                                  s=len(t_obs)*(sigma*smooth_factor)**2)
        X[i]  = spl(t)
    return X

def build_fourier_matrix(n_components):
    X = np.zeros((len(countries), len(t)))
    for i, c in enumerate(countries):
        y  = GDP.loc[c].values.astype(float)
        yf = fill_gaps(y)
        Y  = fft(yf)
        Yt = np.zeros_like(Y)
        Yt[:n_components] = Y[:n_components]
        if n_components > 1:
            Yt[-(n_components-1):] = Y[-(n_components-1):]
        X[i] = np.real(ifft(Yt))
    return X

def build_wavelet_matrix(wavelet='sym4', lam=0.0):
    X = np.zeros((len(countries), len(t)))
    for i, c in enumerate(countries):
        y  = GDP.loc[c].values.astype(float)
        yf = fill_gaps(y)
        ap, det, ns, n0 = wavedec(yf, wavelet, WAVELET_LEVELS)
        dt = soft_thr(det, lam) if lam > 0 else det
        X[i] = waverec(ap, dt, ns, wavelet, n0)
    return X

# ── 5. FPCA engine ────────────────────────────────────────────
def run_fpca(X, label=''):
    """
    FPCA via SVD on centred data matrix.
    Returns dict with eigenvalues, eigenfunctions, scores.
    """
    mu   = X.mean(axis=0)
    X_c  = X - mu
    U, S, Vt = np.linalg.svd(X_c, full_matrices=False)
    total_var = np.sum(S**2)
    var_exp   = S**2 / total_var * 100
    cumvar    = np.cumsum(var_exp)
    n80       = int(np.argmax(cumvar >= 80)) + 1
    scores    = U * S        # (N, min(N,T)) — PC scores per country
    fpcs      = Vt           # (min(N,T), T) — FPC curves
    return {
        'label':   label,
        'X':       X,
        'mu':      mu,
        'fpcs':    fpcs,
        'scores':  scores,
        'var_exp': var_exp,
        'cumvar':  cumvar,
        'n80':     n80,
    }

# ── 6. Run FPCA for all configurations ───────────────────────
print("\n  Building functional data matrices and running FPCA...\n")

configs = [
    ('Raw data\n(baseline)', build_raw_matrix()),
    ('B-spline\n(smooth σ×2)', build_bspline_matrix(smooth_factor=2.0)),
    ('Fourier\n(5 comp.)',    build_fourier_matrix(5)),
    ('Fourier\n(15 comp.)',   build_fourier_matrix(15)),
    ('Wavelet Sym4\nλ=0 (lossless)', build_wavelet_matrix('sym4', lam=0)),
    ('Wavelet Sym4\nλ=5.0',          build_wavelet_matrix('sym4', lam=5.0)),
    ('Wavelet Sym4\nλ=12.0',         build_wavelet_matrix('sym4', lam=12.0)),
    ('Wavelet DB2\nλ=5.0',           build_wavelet_matrix('db2',  lam=5.0)),
    ('Wavelet Haar\nλ=5.0',          build_wavelet_matrix('haar', lam=5.0)),
]

fpca_results = []
print(f"  {'Configuration':<28} {'FPC1':>6} {'FPC2':>6} {'FPC3':>6} "
      f"{'3-FPC':>7} {'n→80%':>7}")
print("  " + "-" * 63)

for label, X in configs:
    res = run_fpca(X, label)
    fpca_results.append(res)
    v   = res['var_exp']
    lbl = label.replace('\n', ' ')
    print(f"  {lbl:<28} {v[0]:>6.1f} {v[1]:>6.1f} {v[2]:>6.1f} "
          f"{sum(v[:3]):>7.1f} {res['n80']:>7d}")

# ── 7. Figure 1: Variance explained table / bar chart ─────────
labels_short = [r['label'].replace('\n', '\n') for r in fpca_results]
n_fpc_show   = 8
colors_fpc   = plt.cm.Blues(np.linspace(0.3, 0.9, n_fpc_show))

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Left: stacked bar of variance per FPC
x = np.arange(len(fpca_results))
bottoms = np.zeros(len(fpca_results))
for k in range(n_fpc_show):
    vals = [r['var_exp'][k] if k < len(r['var_exp']) else 0
            for r in fpca_results]
    axes[0].bar(x, vals, bottom=bottoms, color=colors_fpc[k],
                label=f'FPC{k+1}', alpha=0.9)
    bottoms += np.array(vals)

axes[0].axhline(80, color='red', lw=1.5, ls='--', label='80% threshold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(labels_short, fontsize=8)
axes[0].set_ylabel("Cumulative Variance Explained (%)", fontsize=11)
axes[0].set_title("Variance Explained by FPCs\nper Basis Configuration",
                   fontsize=11, fontweight='bold')
axes[0].legend(fontsize=8, ncol=2, loc='lower right')
axes[0].set_ylim(0, 105)
axes[0].grid(True, axis='y', alpha=0.3)

# Right: n FPCs needed for 80%
n80_vals = [r['n80'] for r in fpca_results]
bar_colors = ['#607D8B','#607D8B',
              '#FF9800','#F44336',
              '#4CAF50','#2196F3','#1565C0',
              '#9C27B0','#43A047']
axes[1].bar(x, n80_vals, color=bar_colors, alpha=0.85)
axes[1].set_xticks(x)
axes[1].set_xticklabels(labels_short, fontsize=8)
axes[1].set_ylabel("Number of FPCs required", fontsize=11)
axes[1].set_title("FPCs Needed to Explain ≥80% Variance\n"
                   "(fewer = more parsimonious representation)",
                   fontsize=11, fontweight='bold')
for xi, n in zip(x, n80_vals):
    axes[1].text(xi, n + 0.1, str(n), ha='center', fontsize=11,
                 fontweight='bold')
axes[1].set_ylim(0, max(n80_vals) + 2)
axes[1].grid(True, axis='y', alpha=0.3)

fig.suptitle("FPCA Summary: How Many Components Does Each Basis Need?",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig15_fpca_variance_summary.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("\n  Saved: fig15_fpca_variance_summary.png")

# ── 8. Figure 2: FPC curves (perturbation plots) ──────────────
# Replicate Fig 7 from the original paper for 3 key configurations
configs_to_plot = [
    ('Raw data\n(baseline)', fpca_results[0]),
    ('Wavelet Sym4\nλ=5.0',  fpca_results[5]),
    ('Fourier\n(15 comp.)',   fpca_results[3]),
]

fig, axes = plt.subplots(3, 3, figsize=(18, 12))
perturbation_scale = 2.0   # how much to perturb the mean

for col, (cfg_label, res) in enumerate(configs_to_plot):
    mu   = res['mu']
    fpcs = res['fpcs']
    v    = res['var_exp']

    for row in range(3):
        ax    = axes[row][col]
        fpc   = fpcs[row]     # shape (T,)
        fpc_n = fpc / np.max(np.abs(fpc))  # normalise for display

        ax.plot(t, mu, color='green', lw=2,
                label='Mean', zorder=3)
        ax.plot(t, mu + perturbation_scale * fpc_n,
                color='blue', lw=1.5, ls='--',
                label=f'+{perturbation_scale}×FPC', zorder=2)
        ax.plot(t, mu - perturbation_scale * fpc_n,
                color='blue', lw=1.5, ls=':',
                label=f'-{perturbation_scale}×FPC', zorder=2)
        ax.axhline(0, color='black', lw=0.5, ls='--', alpha=0.4)
        for yr in CRISIS_YEARS:
            ax.axvline(yr, color='red', lw=0.5, ls=':', alpha=0.3)

        if row == 0:
            ax.set_title(cfg_label.replace('\n', ' '),
                         fontsize=11, fontweight='bold')
        ax.set_ylabel(f'FPC{row+1}  ({v[row]:.1f}%)', fontsize=9)
        ax.grid(True, alpha=0.25)
        ax.tick_params(labelsize=7)
        if row == 0 and col == 0:
            ax.legend(fontsize=7, loc='upper right')

fig.suptitle("Mean Perturbation Plots — FPC1, FPC2, FPC3\n"
             "(Blue dashed = mean + 2×FPC,  dotted = mean − 2×FPC)",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig16_fpc_perturbation_plots.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: fig16_fpc_perturbation_plots.png")

# ── 9. Figure 3: Score plots (replicating Fig 8 of paper) ─────
configs_scores = [
    ('Raw data (baseline)', fpca_results[0],   '#607D8B'),
    ('Wavelet Sym4  λ=5.0', fpca_results[5],   '#9C27B0'),
    ('Fourier 15 comp.',     fpca_results[3],   '#F44336'),
]

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, (cfg_label, res, color) in zip(axes, configs_scores):
    scores = res['scores']
    v      = res['var_exp']
    for i, c in enumerate(countries):
        ax.scatter(scores[i, 0], scores[i, 1],
                   color=PALETTE[i], s=60, zorder=3)
        ax.annotate(short[c], (scores[i,0], scores[i,1]),
                    fontsize=6.5, ha='left', va='bottom',
                    xytext=(3, 2), textcoords='offset points')
    ax.axhline(0, color='black', lw=0.6, ls='--', alpha=0.4)
    ax.axvline(0, color='black', lw=0.6, ls='--', alpha=0.4)
    ax.set_xlabel(f'PC Score 1  ({v[0]:.1f}%)', fontsize=10)
    ax.set_ylabel(f'PC Score 2  ({v[1]:.1f}%)', fontsize=10)
    ax.set_title(cfg_label, fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.25)

fig.suptitle("FPCA Score Plots: PC1 vs PC2 per Country\n"
             "(Separability of countries reflects basis quality)",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig17_fpca_score_plots.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: fig17_fpca_score_plots.png")

# ── 10. Figure 4: Cumulative variance curves ──────────────────
fig, ax = plt.subplots(figsize=(12, 6))
line_styles = [
    ('#607D8B', '-',  'o',  'Raw data (baseline)'),
    ('#607D8B', '--', 's',  'B-spline smooth σ×2'),
    ('#FF9800', '-',  'o',  'Fourier 5 comp.'),
    ('#F44336', '-',  's',  'Fourier 15 comp.'),
    ('#4CAF50', '-',  'o',  'Wavelet Sym4 λ=0 (lossless)'),
    ('#2196F3', '-',  's',  'Wavelet Sym4 λ=5.0'),
    ('#1565C0', '-',  'D',  'Wavelet Sym4 λ=12.0'),
    ('#9C27B0', '--', 'o',  'Wavelet DB2  λ=5.0'),
    ('#43A047', '--', 's',  'Wavelet Haar λ=5.0'),
]

for res, (clr, ls, mk, lbl) in zip(fpca_results, line_styles):
    n_show = min(15, len(res['cumvar']))
    ax.plot(range(1, n_show+1), res['cumvar'][:n_show],
            color=clr, ls=ls, marker=mk, ms=5,
            lw=1.8, label=lbl, alpha=0.85)

ax.axhline(80, color='red', lw=1.2, ls=':', alpha=0.7,
           label='80% threshold')
ax.set_xlabel("Number of Functional Principal Components", fontsize=11)
ax.set_ylabel("Cumulative Variance Explained (%)", fontsize=11)
ax.set_title("Cumulative Variance Explained by Leading FPCs\n"
             "Steeper rise = more parsimonious functional representation",
             fontsize=12, fontweight='bold')
ax.legend(fontsize=8.5, loc='lower right', ncol=2)
ax.set_xlim(1, 15);  ax.set_ylim(0, 102)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig18_cumvar_curves.png", dpi=150)
plt.close()
print("  Saved: fig18_cumvar_curves.png")

# ── 11. Figure 5: FPC1 curve comparison across bases ──────────
# Show what FPC1 "looks like" in each basis — what does it capture?
fig, axes = plt.subplots(3, 3, figsize=(18, 12))
axes = axes.flatten()

for ax, (label, X) in zip(axes, configs):
    res = run_fpca(X, label)
    fpc1 = res['fpcs'][0]
    # Sign convention: flip if FPC1 is mostly negative
    if fpc1.mean() < 0:
        fpc1 = -fpc1
    fpc1_n = fpc1 / np.max(np.abs(fpc1))

    ax.plot(t, fpc1_n, lw=2, color='#1565C0')
    ax.axhline(0, color='black', lw=0.6, ls='--', alpha=0.4)
    for yr in CRISIS_YEARS:
        ax.axvline(yr, color='red', lw=0.5, ls=':', alpha=0.3)
        ax.text(yr+0.5, -0.85, list(CRISIS_YEARS.values())[
            list(CRISIS_YEARS.keys()).index(yr)][:4],
            fontsize=6, color='red', alpha=0.7)
    ax.set_title(f"{label.replace(chr(10),' ')}  —  "
                 f"FPC1 = {res['var_exp'][0]:.1f}%",
                 fontsize=9, fontweight='bold')
    ax.set_ylim(-1.1, 1.1)
    ax.grid(True, alpha=0.25)
    ax.tick_params(labelsize=7)

fig.suptitle("FPC1 Shape across All Basis Configurations\n"
             "(Normalised to [-1, 1]; shows what variation FPC1 captures)",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig19_fpc1_shapes.png", dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: fig19_fpc1_shapes.png")

# ── 12. Summary table ─────────────────────────────────────────
print("\n" + "=" * 65)
print("  FPCA SUMMARY TABLE  (replicates & extends paper Table 2)")
print("=" * 65)
print(f"\n  {'Configuration':<28} {'FPC1':>6} {'FPC2':>6} "
      f"{'FPC3':>6} {'3-FPC':>7} {'n→80%':>7}")
print("  " + "─" * 60)
for res in fpca_results:
    v   = res['var_exp']
    lbl = res['label'].replace('\n', ' ')
    print(f"  {lbl:<28} {v[0]:>6.1f} {v[1]:>6.1f} {v[2]:>6.1f} "
          f"{sum(v[:3]):>7.1f} {res['n80']:>7d}")

print("\n  ORIGINAL PAPER (Padilla-Segarra et al. 2020):")
print(f"  {'B-spline order 5, dim 48':<28} {'17.7':>6} {'16.5':>6} "
      f"{'12.9':>6} {'47.1':>7} {'>8':>7}")

print("\n" + "=" * 65)
print(f"  Figures saved to: {OUTPUT_DIR}/")
print("=" * 65)