# ============================================================
# Thesis: Comparative Analysis of Functional Bases for
#         Volatile Economic Series
# Script 02: Basis Expansions — B-splines, Fourier, Wavelets
# Author: Esteban Quiña
# ============================================================
# Run with fda_env active from your project root:
#   python smoothing/02_basis_expansions.py
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import convolve
from pathlib import Path

# ── 0. Configuration ─────────────────────────────────────────
DATA_PATH  = Path("smoothing/latin_america_gdp_growth.csv")
OUTPUT_DIR = Path("smoothing/output/02_basis_expansions")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CRISIS_YEARS     = {1982: "Debt Crisis", 1999: "LatAm Crises",
                    2008: "GFC",         2020: "COVID-19"}
FOURIER_COMPS    = [5, 10, 15]
WAVELET_FAMILIES = ['haar', 'db4', 'sym4']
WAVELET_LEVELS   = 4

# ── 1. Load data ──────────────────────────────────────────────
df_raw    = pd.read_csv(DATA_PATH)
years     = list(range(1960, 2025))
countries = df_raw["economy"].tolist()
names     = dict(zip(df_raw["economy"], df_raw["Country"]))

GDP = df_raw.set_index("economy").drop(columns="Country")
GDP.columns = [int(c.replace("YR", "")) for c in GDP.columns]
GDP = GDP[years]
t   = np.array(years, dtype=float)

print("=" * 60)
print("  Script 02: Basis Expansions  (fixed)")
print("=" * 60)

# ── 2. Gap-fill helper ────────────────────────────────────────
def fill_gaps(y):
    """Linear interp + ffill/bfill for leading/trailing NaNs."""
    return pd.Series(y).interpolate(method='linear').ffill().bfill().values

# ── 3. Wavelet infrastructure (no pywt) ──────────────────────
FILTERS = {
    'haar': {
        'lo': np.array([1.0, 1.0]) / np.sqrt(2),
        'hi': np.array([-1.0, 1.0]) / np.sqrt(2),
    },
    'db4': {
        'lo': np.array([
            -0.010597401785069032, -0.032883011666999545,
             0.030841381835560764,  0.187034811718881140,
            -0.027983769416983862, -0.630880767929590400,
             0.714846570552541500,  0.230377813308855230]),
        'hi': np.array([
            -0.230377813308855230,  0.714846570552541500,
             0.630880767929590400, -0.027983769416983862,
            -0.187034811718881140,  0.030841381835560764,
             0.032883011666999545, -0.010597401785069032]),
    },
    'sym4': {
        'lo': np.array([
            -0.075765714789356680, -0.029635527645960390,
             0.497618667632562900,  0.803738751805914900,
             0.297857795605605050, -0.099219543576947200,
            -0.012603967262030850,  0.032223100604078150]),
        'hi': np.array([
            -0.032223100604078150, -0.012603967262030850,
             0.099219543576947200,  0.297857795605605050,
            -0.803738751805914900,  0.497618667632562900,
             0.029635527645960390, -0.075765714789356680]),
    }
}


def _dwt_single(signal, lo, hi):
    n   = len(signal)
    app = convolve(signal, lo[::-1], mode='full')[len(lo)-1:n+len(lo)-1:2]
    det = convolve(signal, hi[::-1], mode='full')[len(hi)-1:n+len(hi)-1:2]
    k   = n // 2
    return app[:k], det[:k]


def wavedec(signal, wavelet='db4', levels=4):
    lo, hi  = FILTERS[wavelet]['lo'], FILTERS[wavelet]['hi']
    n_orig  = len(signal)
    n_pad   = int(2 ** np.ceil(np.log2(n_orig)))
    sig     = np.pad(signal.astype(float), (0, n_pad - n_orig), mode='reflect')
    coeffs  = []
    cur     = sig
    for _ in range(levels):
        cur, det = _dwt_single(cur, lo, hi)
        coeffs.append(det)
    coeffs.append(cur)
    return coeffs[::-1], n_orig   # [approx, coarse→fine details]


def _idwt_single(approx, detail, lo, hi, n_out):
    lo_r = lo[::-1];  hi_r = hi[::-1]
    up_a = np.zeros(2 * len(approx));  up_a[::2] = approx
    up_d = np.zeros(2 * len(detail));  up_d[::2] = detail
    rec  = (convolve(up_a, lo_r, mode='full') +
            convolve(up_d, hi_r, mode='full'))
    offset = len(lo_r) - 1
    return rec[offset: offset + n_out]


def waverec(coeffs, wavelet, n_orig):
    lo, hi = FILTERS[wavelet]['lo'], FILTERS[wavelet]['hi']
    cur    = coeffs[0].copy()
    for det in coeffs[1:]:
        n_out = min(2 * len(cur), 2 * len(det))
        cur   = _idwt_single(cur, det, lo, hi, n_out)
    return cur[:n_orig]


def soft_threshold(coeffs, lam):
    out = [coeffs[0].copy()]
    for c in coeffs[1:]:
        out.append(np.sign(c) * np.maximum(np.abs(c) - lam, 0))
    return out


def hard_threshold(coeffs, lam):
    out = [coeffs[0].copy()]
    for c in coeffs[1:]:
        out.append(c * (np.abs(c) >= lam))
    return out

# ── 4. Basis expansion functions ──────────────────────────────

def bspline_smooth(t, y, degree=3):
    """
    B-spline with data-driven smoothing.
    s = n * sigma^2  where sigma is a robust noise estimate.
    This makes the smoothing adapt to each country's volatility.
    Bug fix: previous version used s = smooth * N = constant,
    giving identical RMSE = sqrt(smooth) = 0.707 for all countries.
    """
    mask = ~np.isnan(y)
    t_obs, y_obs = t[mask], y[mask]
    diffs  = np.diff(y_obs)
    # Robust scale estimate via MAD
    sigma  = np.median(np.abs(diffs - np.median(diffs))) / 0.6745 / np.sqrt(2)
    sigma  = max(sigma, 0.1)       # floor for very smooth series
    s_val  = len(t_obs) * sigma**2
    spl    = UnivariateSpline(t_obs, y_obs, k=degree, s=s_val)
    return spl(t), spl, s_val, sigma


def fourier_smooth(t, y, n_components):
    """
    Fourier basis retaining n_components lowest-frequency terms.
    Bug fix: use fill_gaps() to handle leading/trailing NaNs
    (plain interpolate() left the first observation as NaN → FFT produced NaN).
    """
    y_full  = fill_gaps(y)          # ← fix
    N       = len(y_full)
    Y       = fft(y_full)
    Y_trunc = np.zeros_like(Y)
    Y_trunc[:n_components] = Y[:n_components]
    if n_components > 1:
        Y_trunc[-(n_components - 1):] = Y[-(n_components - 1):]
    y_rec = np.real(ifft(Y_trunc))
    return y_rec, Y


def wavelet_smooth(y, wavelet='db4', levels=4, threshold=None, mode='soft'):
    """
    Wavelet decomposition and optional soft/hard thresholding.
    Bug fix: same fill_gaps() fix as Fourier — leading NaNs (Cuba, El Salvador)
    caused NaN to propagate through the convolutions.
    """
    y_full = fill_gaps(y)           # ← fix
    coeffs, n_orig = wavedec(y_full, wavelet=wavelet, levels=levels)
    if threshold is not None:
        coeffs_thr = (soft_threshold(coeffs, threshold) if mode == 'soft'
                      else hard_threshold(coeffs, threshold))
    else:
        coeffs_thr = coeffs
    y_rec = waverec(coeffs_thr, wavelet, n_orig)
    return y_rec, coeffs, coeffs_thr

# ── 5. RMSE ───────────────────────────────────────────────────
def rmse(y_true, y_pred):
    mask = ~np.isnan(y_true)
    if mask.sum() == 0:
        return np.nan
    return np.sqrt(np.mean((y_true[mask] - y_pred[mask]) ** 2))

def safe_mean(vals):
    v = [x for x in vals if not np.isnan(x)]
    return np.mean(v) if v else np.nan

# ── 6. Run expansions ─────────────────────────────────────────
results = []
print(f"\n  {'Code':<5} {'σ-est':>7} {'B-spl RMSE':>11} "
      f"{'DB4 RMSE':>10} {'F-10 RMSE':>10}")
print("  " + "-" * 50)

for country in countries:
    y    = GDP.loc[country].values.astype(float)
    name = names[country]

    y_bsp, spl, s_val, sigma = bspline_smooth(t, y)
    rmse_bsp = rmse(y, y_bsp)

    fourier_results = {}
    for nc in FOURIER_COMPS:
        y_f, Y = fourier_smooth(t, y, n_components=nc)
        fourier_results[nc] = {'y_rec': y_f, 'rmse': rmse(y, y_f), 'Y': Y}

    wavelet_results = {}
    for wv in WAVELET_FAMILIES:
        y_w, coeffs, _ = wavelet_smooth(y, wavelet=wv, levels=WAVELET_LEVELS)
        wavelet_results[wv] = {
            'y_rec':   y_w,
            'rmse':    rmse(y, y_w),
            'coeffs':  coeffs,
            'n_total': sum(len(c) for c in coeffs),
        }

    results.append({
        'economy':  country, 'name': name, 'y_obs': y,
        'sigma':    sigma,   'bsp':  y_bsp, 'rmse_bsp': rmse_bsp,
        'fourier':  fourier_results, 'wavelet': wavelet_results,
    })

    print(f"  {country:<5} {sigma:>7.2f} {rmse_bsp:>11.4f} "
          f"{wavelet_results['db4']['rmse']:>10.4f} "
          f"{fourier_results[10]['rmse']:>10.4f}")

# ── 7. Figure 1: 4×4 comparison grid ─────────────────────────
showcase    = ['VEN', 'ARG', 'COL', 'BRA']
col_titles  = ['B-spline (adaptive)', 'Fourier (10 comp.)',
               'Wavelet Haar',        'Wavelet DB4']
base_colors = ['#2196F3', '#FF5722', '#4CAF50', '#9C27B0']

fig, axes = plt.subplots(4, 4, figsize=(20, 16))
for row, c in enumerate(showcase):
    r     = next(x for x in results if x['economy'] == c)
    y_obs = r['y_obs']
    recs  = [r['bsp'], r['fourier'][10]['y_rec'],
             r['wavelet']['haar']['y_rec'], r['wavelet']['db4']['y_rec']]
    rmses = [r['rmse_bsp'], r['fourier'][10]['rmse'],
             r['wavelet']['haar']['rmse'], r['wavelet']['db4']['rmse']]

    for col, (y_rec, rm, ttl, clr) in enumerate(
            zip(recs, rmses, col_titles, base_colors)):
        ax = axes[row][col]
        ax.plot(t, y_obs, 'o', color='gray', ms=2.5,
                alpha=0.65, label='Observed', zorder=2)
        ax.plot(t, y_rec, lw=1.8, color=clr,
                label=f'RMSE={rm:.3f}', zorder=3)
        ax.axhline(0, color='black', lw=0.6, ls='--', alpha=0.4)
        for yr in CRISIS_YEARS:
            ax.axvline(yr, color='red', lw=0.5, ls=':', alpha=0.35)
        if row == 0:
            ax.set_title(ttl, fontsize=11, fontweight='bold')
        if col == 0:
            ax.set_ylabel(r['name'], fontsize=9, fontweight='bold')
        ax.legend(fontsize=7, loc='upper right')
        ax.grid(True, alpha=0.25)
        ax.tick_params(labelsize=7)

fig.suptitle("Basis Expansions: B-spline vs Fourier vs Wavelets\n"
             "(4 Representative Countries)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig07_basis_comparison_grid.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("\n  Saved: fig07_basis_comparison_grid.png")

# ── 8. Figure 2: RMSE bar chart ───────────────────────────────
df_m = pd.DataFrame([{
    'Country':    r['name'],
    'B-spline':   r['rmse_bsp'],
    'Fourier 5':  r['fourier'][5]['rmse'],
    'Fourier 10': r['fourier'][10]['rmse'],
    'Fourier 15': r['fourier'][15]['rmse'],
    'Haar':       r['wavelet']['haar']['rmse'],
    'DB4':        r['wavelet']['db4']['rmse'],
    'Sym4':       r['wavelet']['sym4']['rmse'],
} for r in results]).set_index('Country')

fig, ax = plt.subplots(figsize=(14, 7))
x = np.arange(len(df_m));  w = 0.11
cols_p  = ['B-spline','Fourier 5','Fourier 10','Fourier 15',
           'Haar','DB4','Sym4']
clrs_p  = ['#607D8B','#FF9800','#F44336','#E91E63',
           '#4CAF50','#2196F3','#9C27B0']
for i, (col, clr) in enumerate(zip(cols_p, clrs_p)):
    ax.bar(x + i*w, df_m[col], w, label=col, color=clr, alpha=0.85)
ax.set_xticks(x + 3*w)
ax.set_xticklabels(df_m.index, rotation=45, ha='right', fontsize=8)
ax.set_ylabel("RMSE (percentage points)", fontsize=11)
ax.set_title("Reconstruction RMSE by Basis and Country",
             fontsize=13, fontweight='bold')
ax.legend(fontsize=9, ncol=4, loc='upper right')
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig08_rmse_comparison.png", dpi=150)
plt.close()
print("  Saved: fig08_rmse_comparison.png")

# ── 9. Figure 3: Wavelet energy distribution ─────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, c in zip(axes, ['VEN', 'COL', 'ARG']):
    r = next(x for x in results if x['economy'] == c)
    for wv, clr in zip(WAVELET_FAMILIES, ['#4CAF50','#2196F3','#9C27B0']):
        coeffs   = r['wavelet'][wv]['coeffs']
        energies = [np.sum(c**2) for c in coeffs]
        total_e  = sum(energies)
        pct      = [e / total_e * 100 for e in energies]
        levels   = ([f'A{WAVELET_LEVELS}'] +
                    [f'D{WAVELET_LEVELS-i}' for i in range(len(coeffs)-1)])
        ax.plot(levels, pct, marker='o', lw=1.8,
                color=clr, label=wv.upper(), alpha=0.85)
    ax.set_title(names[c], fontsize=10, fontweight='bold')
    ax.set_xlabel("Wavelet Level", fontsize=9)
    ax.set_ylabel("Energy (%)", fontsize=9)
    ax.legend(fontsize=9);  ax.grid(True, alpha=0.3)

fig.suptitle("Wavelet Energy Distribution by Level  "
             "(A=Approximation, D=Detail)",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig09_wavelet_energy.png", dpi=150)
plt.close()
print("  Saved: fig09_wavelet_energy.png")

# ── 10. Figure 4: Fourier spectrum — Venezuela ────────────────
r_ven  = next(x for x in results if x['economy'] == 'VEN')
y_ven  = r_ven['y_obs'].copy()
y_full = fill_gaps(y_ven)
N      = len(y_full)
freqs  = fftfreq(N, d=1.0)
Y      = fft(y_full)
pos    = freqs[:N//2] > 0
power  = np.abs(Y[:N//2])**2
periods = 1.0 / freqs[:N//2][pos]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(periods, power[pos], color='#2196F3', lw=1.5)
axes[0].set_xlim([2, 65])
axes[0].set_xlabel("Period (years)", fontsize=11)
axes[0].set_ylabel("Power", fontsize=11)
axes[0].set_title("Power Spectrum — Venezuela GDP Growth",
                  fontsize=11, fontweight='bold')
axes[0].grid(True, alpha=0.3)

for nc, clr in zip(FOURIER_COMPS, ['#FF9800','#F44336','#9C27B0']):
    rm = r_ven['fourier'][nc]['rmse']
    axes[1].plot(t, r_ven['fourier'][nc]['y_rec'], lw=1.5,
                 color=clr, label=f'{nc} comp.  RMSE={rm:.2f}')
axes[1].plot(t, y_ven, 'o', color='gray', ms=2.5,
             alpha=0.7, label='Observed', zorder=5)
axes[1].axhline(0, color='black', lw=0.6, ls='--', alpha=0.4)
for yr in CRISIS_YEARS:
    axes[1].axvline(yr, color='red', lw=0.5, ls=':', alpha=0.4)
axes[1].set_title("Fourier Reconstructions — Venezuela",
                  fontsize=11, fontweight='bold')
axes[1].set_xlabel("Year", fontsize=11)
axes[1].set_ylabel("GDP Growth Rate (%)", fontsize=11)
axes[1].legend(fontsize=9);  axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig10_fourier_spectrum_venezuela.png", dpi=150)
plt.close()
print("  Saved: fig10_fourier_spectrum_venezuela.png")

# ── 11. Figure 5: Wavelet thresholding — Venezuela ────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, (lam, label) in zip(axes, [
        (None, 'No threshold\n(full reconstruction)'),
        (1.0,  'Soft threshold  λ=1.0'),
        (2.5,  'Soft threshold  λ=2.5')]):
    y_w, coeffs, coeffs_thr = wavelet_smooth(
        y_ven, wavelet='db4', levels=WAVELET_LEVELS,
        threshold=lam, mode='soft')
    n_nz  = sum(np.count_nonzero(c) for c in coeffs_thr)
    n_tot = sum(len(c) for c in coeffs_thr)
    rm    = rmse(y_ven, y_w)
    ax.plot(t, y_ven, 'o', color='gray', ms=3, alpha=0.7,
            label='Observed', zorder=2)
    ax.plot(t, y_w, lw=2, color='#2196F3',
            label=f'RMSE={rm:.3f}  NZ={n_nz}/{n_tot}', zorder=3)
    ax.axhline(0, color='black', lw=0.6, ls='--', alpha=0.4)
    for yr in CRISIS_YEARS:
        ax.axvline(yr, color='red', lw=0.5, ls=':', alpha=0.4)
    ax.set_title(label, fontsize=10, fontweight='bold')
    ax.set_xlabel("Year", fontsize=9)
    ax.set_ylabel("GDP Growth (%)", fontsize=9)
    ax.legend(fontsize=8);  ax.grid(True, alpha=0.3)

fig.suptitle("DB4 Wavelet Thresholding — Venezuela GDP Growth",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig11_wavelet_thresholding.png", dpi=150)
plt.close()
print("  Saved: fig11_wavelet_thresholding.png")

# ── 12. Summary table ─────────────────────────────────────────
print("\n" + "=" * 60)
print("  SUMMARY: Mean RMSE across all 20 countries")
print("=" * 60)
summary = {
    'B-spline (adaptive)': safe_mean([r['rmse_bsp'] for r in results]),
    'Fourier   5 comp.  ': safe_mean([r['fourier'][5]['rmse']  for r in results]),
    'Fourier  10 comp.  ': safe_mean([r['fourier'][10]['rmse'] for r in results]),
    'Fourier  15 comp.  ': safe_mean([r['fourier'][15]['rmse'] for r in results]),
    'Wavelet  Haar      ': safe_mean([r['wavelet']['haar']['rmse'] for r in results]),
    'Wavelet  DB4       ': safe_mean([r['wavelet']['db4']['rmse']  for r in results]),
    'Wavelet  Sym4      ': safe_mean([r['wavelet']['sym4']['rmse'] for r in results]),
}
best = min(summary.values())
for method, val in summary.items():
    bar  = '█' * int(round(val / best * 10))
    flag = '  ← best' if abs(val - best) < 0.001 else ''
    print(f"  {method}: {val:.4f}  {bar}{flag}")

print("\n" + "=" * 60)
print("  All figures saved to: smoothing/output/02_basis_expansions/")
print("=" * 60)