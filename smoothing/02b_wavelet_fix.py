# ============================================================
# Thesis: Comparative Analysis of Functional Bases for
#         Volatile Economic Series
# Script 02b: Wavelet Reconstruction — Corrected Pipeline
# Author: Esteban Quiña
# ============================================================
# Key corrections from 02:
#  1. Matrix DWT (explicit orthogonal W) — exact round-trip
#  2. DB4 → DB2 (length-4 filter, exact at all decomp levels)
#  3. Correct comparison framework:
#       Wavelets evaluated at lambda that matches B-spline RMSE
#       → "same reconstruction quality, how many coefficients?"
#       This is the direct empirical test of the Besov argument.
#  4. Summary table uses finite values only (no division by zero)
# ============================================================
# Run:  python smoothing/02b_wavelet_fix.py
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
OUTPUT_DIR = Path("smoothing/output/02b_wavelet_fix")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CRISIS_YEARS     = {1982: "Debt Crisis", 1999: "LatAm Crises",
                    2008: "GFC",         2020: "COVID-19"}
FOURIER_COMPS    = [5, 10, 15]
WAVELET_FAMILIES = ['haar', 'db2', 'sym4']
WAVELET_LEVELS   = 4
THR_LAMBDAS      = np.arange(0.5, 15.5, 0.5).tolist()

# ── 1. Load data ──────────────────────────────────────────────
df_raw    = pd.read_csv(DATA_PATH)
years     = list(range(1960, 2025))
countries = df_raw["economy"].tolist()
names     = dict(zip(df_raw["economy"], df_raw["Country"]))

GDP = df_raw.set_index("economy").drop(columns="Country")
GDP.columns = [int(c.replace("YR", "")) for c in GDP.columns]
GDP = GDP[years]
t   = np.array(years, dtype=float)

print("=" * 65)
print("  Script 02b: Wavelet Reconstruction — Corrected Pipeline")
print("=" * 65)

# ── 2. Helpers ────────────────────────────────────────────────
def fill_gaps(y):
    return pd.Series(y).interpolate('linear').ffill().bfill().values

def rmse_obs(y_true, y_pred):
    mask = ~np.isnan(y_true)
    return np.sqrt(np.mean((y_true[mask] - y_pred[mask]) ** 2))

def safe_mean(vals):
    v = [x for x in vals if np.isfinite(x)]
    return np.mean(v) if v else np.nan

# ── 3. Wavelet infrastructure ─────────────────────────────────
_db2_lo = np.array([
    (1 + np.sqrt(3)) / (4*np.sqrt(2)),
    (3 + np.sqrt(3)) / (4*np.sqrt(2)),
    (3 - np.sqrt(3)) / (4*np.sqrt(2)),
    (1 - np.sqrt(3)) / (4*np.sqrt(2))])

def _make_hi(lo):
    N = len(lo)
    return np.array([(-1)**k * lo[N-1-k] for k in range(N)])

_sym4_lo = np.array([
    -0.075765714789356680, -0.029635527645960390,
     0.497618667632562900,  0.803738751805914900,
     0.297857795605605050, -0.099219543576947200,
    -0.012603967262030850,  0.032223100604078150])

FILTERS = {
    'haar': {
        'lo': np.array([1.0, 1.0]) / np.sqrt(2),
        'hi': np.array([-1.0, 1.0]) / np.sqrt(2),
    },
    'db2':  {'lo': _db2_lo,  'hi': _make_hi(_db2_lo)},
    'sym4': {'lo': _sym4_lo, 'hi': _make_hi(_sym4_lo)},
}


def _build_W(n, lo, hi):
    """
    One-level circular DWT matrix (n×n), orthogonal: W @ W.T = I.
    Rows 0..n//2-1     → approximation
    Rows n//2..n-1     → detail
    """
    f = len(lo)
    W = np.zeros((n, n))
    for i in range(n // 2):
        for j in range(f):
            W[i,          (2*i + j) % n] += lo[j]
            W[i + n//2,   (2*i + j) % n] += hi[j]
    return W


def wavedec(y, wavelet='sym4', levels=4):
    """Matrix DWT. Returns (approx, details, level_ns, n_orig)."""
    lo, hi = FILTERS[wavelet]['lo'], FILTERS[wavelet]['hi']
    n_orig = len(y)
    n_pad  = int(2 ** np.ceil(np.log2(n_orig)))
    x      = np.resize(y.astype(float), n_pad)   # circular wrap
    details, level_ns = [], []
    cur = x
    for _ in range(levels):
        n   = len(cur)
        W   = _build_W(n, lo, hi)
        out = W @ cur
        level_ns.append(n)
        details.append(out[n//2:])
        cur = out[:n//2]
    return cur, details, level_ns, n_orig          # approx, [d_J..d_1], sizes


def waverec(approx, details, level_ns, wavelet, n_orig):
    """Exact inverse: W.T @ [approx; detail] at each level."""
    lo, hi = FILTERS[wavelet]['lo'], FILTERS[wavelet]['hi']
    cur = approx.copy()
    for det, n in zip(reversed(details), reversed(level_ns)):
        W   = _build_W(n, lo, hi)
        cur = W.T @ np.concatenate([cur, det])
    return cur[:n_orig]


def soft_threshold(details, lam):
    return [np.sign(d) * np.maximum(np.abs(d) - lam, 0) for d in details]


def reconstruct_at_lambda(y, wavelet, levels, lam):
    """Decompose, threshold at lam, reconstruct. Returns (y_rec, n_nz, n_tot)."""
    yf             = fill_gaps(y)
    ap, det, ns, n0 = wavedec(yf, wavelet, levels)
    det_thr        = soft_threshold(det, lam)
    y_rec          = waverec(ap, det_thr, ns, wavelet, n0)
    n_nz  = sum(np.count_nonzero(d) for d in det_thr) + np.count_nonzero(ap)
    n_tot = sum(len(d) for d in det) + len(ap)
    return y_rec, n_nz, n_tot


# ── 4. B-spline ───────────────────────────────────────────────
def bspline_smooth(t, y, degree=3):
    mask   = ~np.isnan(y)
    t_obs, y_obs = t[mask], y[mask]
    diffs  = np.diff(y_obs)
    sigma  = np.median(np.abs(diffs - np.median(diffs))) / 0.6745 / np.sqrt(2)
    sigma  = max(sigma, 0.1)
    spl    = UnivariateSpline(t_obs, y_obs, k=degree, s=len(t_obs)*sigma**2)
    return spl(t), sigma, len(spl.get_knots())


# ── 5. Fourier ────────────────────────────────────────────────
def fourier_smooth(y, n_components):
    y_full  = fill_gaps(y)
    N       = len(y_full)
    Y       = fft(y_full)
    Y_trunc = np.zeros_like(Y)
    Y_trunc[:n_components] = Y[:n_components]
    if n_components > 1:
        Y_trunc[-(n_components-1):] = Y[-(n_components-1):]
    return np.real(ifft(Y_trunc))


# ── 6. Main loop ──────────────────────────────────────────────
results = []
print(f"\n  {'Code':<5} {'σ':>6} {'B-spl RMSE':>11} {'B-spl knots':>12}")
print("  " + "-" * 40)

for country in countries:
    y    = GDP.loc[country].values.astype(float)
    name = names[country]

    # B-spline
    y_bsp, sigma, n_knots = bspline_smooth(t, y)
    rmse_bsp = rmse_obs(y, y_bsp)

    # Fourier
    fourier_res = {}
    for nc in FOURIER_COMPS:
        y_f = fourier_smooth(y, nc)
        fourier_res[nc] = {'y_rec': y_f, 'rmse': rmse_obs(y, y_f),
                           'n_coeff': 2*nc - 1}   # real FFT coefficient count

    # Wavelets: full threshold sweep
    wavelet_res = {}
    for wv in WAVELET_FAMILIES:
        yf              = fill_gaps(y)
        ap, det, ns, n0 = wavedec(yf, wv, WAVELET_LEVELS)
        n_tot           = sum(len(d) for d in det) + len(ap)

        sweep = []
        for lam in THR_LAMBDAS:
            dt    = soft_threshold(det, lam)
            y_rec = waverec(ap, dt, ns, wv, n0)
            n_nz  = sum(np.count_nonzero(d) for d in dt) + np.count_nonzero(ap)
            sweep.append({
                'lam':       lam,
                'y_rec':     y_rec,
                'rmse':      rmse_obs(y, y_rec),
                'n_nz':      n_nz,
                'n_tot':     n_tot,
                'sparsity':  1 - n_nz / n_tot,
            })

        # Find lambda that best matches B-spline RMSE
        target = rmse_bsp
        matched = min(sweep, key=lambda s: abs(s['rmse'] - target))

        # Energy distribution
        all_c    = [ap] + det
        energies = [np.sum(c**2) for c in all_c]
        tot_e    = sum(energies)
        energy_pct = [e / tot_e * 100 for e in energies]

        wavelet_res[wv] = {
            'sweep':      sweep,
            'matched':    matched,
            'n_tot':      n_tot,
            'ap':         ap,
            'details':    det,
            'energy_pct': energy_pct,
        }

    results.append({
        'economy':  country, 'name': name, 'y_obs': y,
        'sigma':    sigma,   'n_knots': n_knots,
        'bsp':      y_bsp,   'rmse_bsp': rmse_bsp,
        'fourier':  fourier_res,
        'wavelet':  wavelet_res,
    })

    print(f"  {country:<5} {sigma:>6.2f} {rmse_bsp:>11.4f} {n_knots:>12d}")

# ── 7. Figure 1: Corrected 4×4 comparison grid ───────────────
# For wavelets, use the lambda that matches B-spline RMSE per country
showcase    = ['VEN', 'ARG', 'COL', 'BRA']
base_colors = ['#2196F3', '#FF5722', '#4CAF50', '#9C27B0']
col_titles  = ['B-spline (adaptive)', 'Fourier (15 comp.)',
               'Wavelet DB2\n(λ matched to B-spline)',
               'Wavelet Sym4\n(λ matched to B-spline)']

fig, axes = plt.subplots(4, 4, figsize=(20, 16))
for row, c in enumerate(showcase):
    r     = next(x for x in results if x['economy'] == c)
    y_obs = r['y_obs']
    m_db2  = r['wavelet']['db2']['matched']
    m_sym4 = r['wavelet']['sym4']['matched']

    recs  = [r['bsp'],
             r['fourier'][15]['y_rec'],
             m_db2['y_rec'],
             m_sym4['y_rec']]
    labels = [
        f"RMSE={r['rmse_bsp']:.3f}  knots={r['n_knots']}",
        f"RMSE={r['fourier'][15]['rmse']:.3f}  coeff={r['fourier'][15]['n_coeff']}",
        f"RMSE={m_db2['rmse']:.3f}  NZ={m_db2['n_nz']}/{m_db2['n_tot']}",
        f"RMSE={m_sym4['rmse']:.3f}  NZ={m_sym4['n_nz']}/{m_sym4['n_tot']}",
    ]

    for col, (y_rec, lbl, ttl, clr) in enumerate(
            zip(recs, labels, col_titles, base_colors)):
        ax = axes[row][col]
        ax.plot(t, y_obs, 'o', color='gray', ms=2.5,
                alpha=0.65, label='Observed', zorder=2)
        ax.plot(t, y_rec, lw=1.8, color=clr, label=lbl, zorder=3)
        ax.axhline(0, color='black', lw=0.6, ls='--', alpha=0.4)
        for yr in CRISIS_YEARS:
            ax.axvline(yr, color='red', lw=0.5, ls=':', alpha=0.35)
        if row == 0:
            ax.set_title(ttl, fontsize=10, fontweight='bold')
        if col == 0:
            ax.set_ylabel(r['name'], fontsize=9, fontweight='bold')
        ax.legend(fontsize=6.5, loc='upper right')
        ax.grid(True, alpha=0.25)
        ax.tick_params(labelsize=7)

fig.suptitle(
    "Basis Comparison at Equivalent Reconstruction Quality\n"
    "Wavelets thresholded to match B-spline RMSE — labels show coefficient count",
    fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig07b_fair_comparison.png", dpi=150, bbox_inches='tight')
plt.close()
print("\n  Saved: fig07b_fair_comparison.png")

# ── 8. Figure 2: Sparsity at matched RMSE — all 20 countries ─
fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(countries))
w = 0.22

bsp_knots = np.array([r['n_knots'] for r in results])
db2_nz    = np.array([r['wavelet']['db2']['matched']['n_nz']  for r in results])
sym4_nz   = np.array([r['wavelet']['sym4']['matched']['n_nz'] for r in results])
totals    = np.array([r['wavelet']['sym4']['matched']['n_tot'] for r in results])

ax.bar(x - w, bsp_knots,  w, label='B-spline (knots)',
       color='#607D8B', alpha=0.9)
ax.bar(x,     db2_nz,     w, label='DB2 (nonzero coeff, matched RMSE)',
       color='#2196F3', alpha=0.9)
ax.bar(x + w, sym4_nz,    w, label='Sym4 (nonzero coeff, matched RMSE)',
       color='#9C27B0', alpha=0.9)

ax.set_xticks(x)
ax.set_xticklabels([names[c] for c in countries],
                   rotation=45, ha='right', fontsize=8)
ax.set_ylabel("Number of Coefficients Used", fontsize=11)
ax.set_title(
    "Coefficient Economy at Equivalent RMSE\n"
    "Fewer coefficients = sparser representation = Besov space advantage",
    fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig12_coefficient_economy.png", dpi=150)
plt.close()
print("  Saved: fig12_coefficient_economy.png")

# ── 9. Figure 3: RMSE vs sparsity curves ─────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
showcase_thr = ['VEN', 'ARG', 'COL', 'GTM']
thr_colors   = {'VEN':'#E53935','ARG':'#1E88E5','COL':'#43A047','GTM':'#FB8C00'}

for wv, ax in zip(['db2', 'sym4'], axes):
    for c in showcase_thr:
        r     = next(x for x in results if x['economy'] == c)
        sweep = r['wavelet'][wv]['sweep']
        rmses      = [s['rmse']     for s in sweep]
        sparsities = [s['sparsity'] for s in sweep]
        ax.plot(sparsities, rmses, lw=2,
                color=thr_colors[c], label=names[c], alpha=0.85)
        # Mark λ=0 (no threshold → perfect reconstruction, RMSE=0)
        ax.plot(0, 0, 's', color=thr_colors[c], ms=8, zorder=5)
        # Mark B-spline RMSE target
        bsp_rm = next(x for x in results if x['economy'] == c)['rmse_bsp']
        matched = r['wavelet'][wv]['matched']
        ax.plot(matched['sparsity'], matched['rmse'], 'D',
                color=thr_colors[c], ms=7, zorder=5)

    ax.axhline(0, color='black', lw=0.6, ls='--', alpha=0.3)
    ax.set_xlabel("Sparsity (fraction of coefficients zeroed)", fontsize=11)
    ax.set_ylabel("RMSE (percentage points)", fontsize=11)
    ax.set_title(f"{wv.upper()} Wavelet: RMSE vs Sparsity",
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.97,
            "◆ = B-spline RMSE target\n□ = perfect reconstruction (λ=0)",
            transform=ax.transAxes, fontsize=8, va='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

fig.suptitle("Sparsity–Fidelity Tradeoff under Soft Thresholding",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig13_sparsity_fidelity.png", dpi=150)
plt.close()
print("  Saved: fig13_sparsity_fidelity.png")

# ── 10. Figure 4: Wavelet energy distribution ─────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, c in zip(axes, ['VEN', 'COL', 'ARG']):
    r = next(x for x in results if x['economy'] == c)
    for wv, clr in zip(WAVELET_FAMILIES, ['#4CAF50','#2196F3','#9C27B0']):
        pct    = r['wavelet'][wv]['energy_pct']
        levels = ([f'A{WAVELET_LEVELS}'] +
                  [f'D{WAVELET_LEVELS-i}' for i in range(WAVELET_LEVELS)])
        ax.plot(levels, pct, marker='o', lw=1.8,
                color=clr, label=wv.upper(), alpha=0.85)
    ax.set_title(names[c], fontsize=10, fontweight='bold')
    ax.set_xlabel("Decomposition Level", fontsize=9)
    ax.set_ylabel("Energy (%)", fontsize=9)
    ax.legend(fontsize=9);  ax.grid(True, alpha=0.3)

fig.suptitle("Wavelet Energy Distribution  (A=Approximation, D=Detail coarse→fine)",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig09b_energy_distribution.png", dpi=150)
plt.close()
print("  Saved: fig09b_energy_distribution.png")

# ── 11. Figure 5: Visual comparison at matched lambda ─────────
# Venezuela: show B-spline vs Sym4 at matched RMSE side by side
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
r_ven   = next(x for x in results if x['economy'] == 'VEN')
y_ven   = r_ven['y_obs']
m_sym4  = r_ven['wavelet']['sym4']['matched']

panels = [
    (r_ven['bsp'],        f"B-spline  RMSE={r_ven['rmse_bsp']:.3f}  knots={r_ven['n_knots']}",   '#2196F3'),
    (m_sym4['y_rec'],     f"Sym4  RMSE={m_sym4['rmse']:.3f}  NZ={m_sym4['n_nz']}/{m_sym4['n_tot']}", '#9C27B0'),
    (r_ven['fourier'][15]['y_rec'],
     f"Fourier-15  RMSE={r_ven['fourier'][15]['rmse']:.3f}  coeff=29", '#FF5722'),
]
for ax, (y_rec, lbl, clr) in zip(axes, panels):
    ax.plot(t, y_ven, 'o', color='gray', ms=3, alpha=0.7,
            label='Observed', zorder=2)
    ax.plot(t, y_rec, lw=2, color=clr, label=lbl, zorder=3)
    ax.axhline(0, color='black', lw=0.6, ls='--', alpha=0.4)
    for yr in CRISIS_YEARS:
        ax.axvline(yr, color='red', lw=0.5, ls=':', alpha=0.4)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("GDP Growth (%)", fontsize=10)
    ax.legend(fontsize=8, loc='lower left');  ax.grid(True, alpha=0.3)

fig.suptitle("Venezuela — Basis Comparison at Equivalent Reconstruction Quality",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig14_venezuela_comparison.png", dpi=150)
plt.close()
print("  Saved: fig14_venezuela_comparison.png")

# ── 12. Summary ───────────────────────────────────────────────
print("\n" + "=" * 65)
print("  SUMMARY: Mean RMSE and coefficient use across all 20 countries")
print("=" * 65)
print(f"\n  {'Method':<28} {'Mean RMSE':>10}  {'Mean NZ coeff':>14}")
print("  " + "-" * 57)

mean_bsp_rmse   = safe_mean([r['rmse_bsp'] for r in results])
mean_bsp_knots  = safe_mean([r['n_knots']  for r in results])
mean_f15_rmse   = safe_mean([r['fourier'][15]['rmse'] for r in results])
mean_db2_rmse   = safe_mean([r['wavelet']['db2']['matched']['rmse']  for r in results])
mean_db2_nz     = safe_mean([r['wavelet']['db2']['matched']['n_nz']  for r in results])
mean_sym4_rmse  = safe_mean([r['wavelet']['sym4']['matched']['rmse'] for r in results])
mean_sym4_nz    = safe_mean([r['wavelet']['sym4']['matched']['n_nz'] for r in results])
mean_n_tot      = safe_mean([r['wavelet']['sym4']['matched']['n_tot'] for r in results])

print(f"  {'B-spline (adaptive)':<28} {mean_bsp_rmse:>10.4f}  {mean_bsp_knots:>14.1f} knots")
print(f"  {'Fourier 15 components':<28} {mean_f15_rmse:>10.4f}  {'29':>14} coeff")
print(f"  {'DB2  (λ matched to B-spl)':<28} {mean_db2_rmse:>10.4f}  {mean_db2_nz:>14.1f} / {mean_n_tot:.0f}")
print(f"  {'Sym4 (λ matched to B-spl)':<28} {mean_sym4_rmse:>10.4f}  {mean_sym4_nz:>14.1f} / {mean_n_tot:.0f}")

sym4_saving = (1 - mean_sym4_nz / mean_n_tot) * 100
print(f"\n  → At equivalent RMSE, Sym4 uses {mean_sym4_nz:.0f}/{mean_n_tot:.0f} coefficients")
print(f"    ({sym4_saving:.0f}% compression) vs B-spline's {mean_bsp_knots:.0f} knots")
print(f"\n  → This is the empirical Besov space advantage.")
print("\n" + "=" * 65)
print(f"  Figures saved to: {OUTPUT_DIR}/")
print("=" * 65)