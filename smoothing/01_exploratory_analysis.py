# ============================================================
# Thesis: Comparative Analysis of Functional Bases for
#         Volatile Economic Series
# Script 01: Exploratory Data Analysis
# Author: Esteban Quiña
# ============================================================
# Run this script from your project root with fda_env active:
#   source fda_env/bin/activate
#   python smoothing/01_exploratory_analysis.py
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from pathlib import Path

# ── 0. Configuration ─────────────────────────────────────────
DATA_PATH   = Path("smoothing/latin_america_gdp_growth.csv")
OUTPUT_DIR  = Path("smoothing/output/01_exploratory")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Color palette (one color per country)
PALETTE = sns.color_palette("tab20", 20)

# ── 1. Load and reshape data ──────────────────────────────────
df_raw = pd.read_csv(DATA_PATH)

# Melt to long format
df = df_raw.melt(
    id_vars=["economy", "Country"],
    var_name="year_col",
    value_name="gdp_growth"
)
df["year"] = df["year_col"].str.replace("YR", "").astype(int)
df = df.drop(columns="year_col").sort_values(["economy", "year"])

# Wide matrix: rows = countries, cols = years
years    = sorted(df["year"].unique())
countries = df_raw["economy"].tolist()
names     = dict(zip(df_raw["economy"], df_raw["Country"]))

GDP = df.pivot(index="economy", columns="year", values="gdp_growth")
GDP = GDP.loc[countries, years]   # preserve original order

print("=" * 55)
print("  GDP Growth Data Summary")
print("=" * 55)
print(f"  Countries : {len(countries)}")
print(f"  Time span : {years[0]} – {years[-1]}  ({len(years)} years)")
print(f"\n  Missing values per country:")
for c in countries:
    n_miss = GDP.loc[c].isna().sum()
    if n_miss:
        print(f"    {c:4s} ({names[c]:<30s}): {n_miss} missing")
print()

# ── 2. Basic descriptive statistics ──────────────────────────
print("  Descriptive statistics (all countries, all years):")
flat = GDP.values.flatten()
flat = flat[~np.isnan(flat)]
print(f"    Mean   : {flat.mean():.3f}%")
print(f"    Std    : {flat.std():.3f}%")
print(f"    Min    : {flat.min():.3f}%")
print(f"    Max    : {flat.max():.3f}%")
print(f"    Median : {np.median(flat):.3f}%")
print()

# Per-country volatility (std deviation)
vol = GDP.std(axis=1).sort_values(ascending=False)
print("  Country volatility (std of annual growth rate):")
for c, v in vol.items():
    print(f"    {c:4s}  {names[c]:<30s}  σ = {v:.2f}%")
print()

# ── 3. Figure 1: All GDP growth trajectories ─────────────────
fig, ax = plt.subplots(figsize=(14, 6))
for i, c in enumerate(countries):
    row = GDP.loc[c]
    ax.plot(row.index, row.values, color=PALETTE[i],
            linewidth=0.9, alpha=0.75, label=names[c])

ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)

# Mark major crisis years
crises = {1982: "Debt Crisis", 1999: "LatAm\nCrises",
          2008: "GFC", 2020: "COVID-19"}
for yr, label in crises.items():
    ax.axvline(yr, color="red", linewidth=0.7, linestyle=":", alpha=0.6)
    ax.text(yr + 0.2, ax.get_ylim()[0] + 1, label,
            fontsize=7, color="red", alpha=0.8)

ax.set_title("GDP Growth Rate — 20 Latin American Countries (1960–2024)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("GDP Growth Rate (%)", fontsize=11)
ax.legend(loc="upper right", fontsize=6, ncol=2,
          framealpha=0.7, bbox_to_anchor=(1.18, 1))
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig01_all_trajectories.png", dpi=150,
            bbox_inches="tight")
plt.close()
print("  Saved: fig01_all_trajectories.png")

# ── 4. Figure 2: Mean ± std band ─────────────────────────────
mean_curve = GDP.mean(axis=0)
std_curve  = GDP.std(axis=0)

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(years,
                mean_curve - std_curve,
                mean_curve + std_curve,
                alpha=0.25, color="steelblue", label="±1 Std Dev")
ax.plot(years, mean_curve, color="steelblue",
        linewidth=2, label="Regional Mean")
ax.axhline(0, color="black", linewidth=0.7, linestyle="--")

for yr in crises:
    ax.axvline(yr, color="red", linewidth=0.7, linestyle=":", alpha=0.6)

ax.set_title("Regional Mean GDP Growth with Variability Band",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("GDP Growth Rate (%)", fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig02_mean_std_band.png", dpi=150)
plt.close()
print("  Saved: fig02_mean_std_band.png")

# ── 5. Figure 3: Country volatility bar chart ─────────────────
fig, ax = plt.subplots(figsize=(12, 5))
vol_sorted = vol.sort_values(ascending=True)
colors_bar = [PALETTE[countries.index(c)] for c in vol_sorted.index]
bars = ax.barh([names[c] for c in vol_sorted.index],
               vol_sorted.values, color=colors_bar, alpha=0.85)
ax.set_xlabel("Standard Deviation of GDP Growth Rate (%)", fontsize=11)
ax.set_title("Country-Level Volatility of GDP Growth (1960–2024)",
             fontsize=13, fontweight="bold")
ax.axvline(vol.mean(), color="red", linestyle="--",
           linewidth=1.2, label=f"Mean σ = {vol.mean():.2f}%")
ax.legend(fontsize=10)
ax.grid(True, axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig03_volatility_bars.png", dpi=150)
plt.close()
print("  Saved: fig03_volatility_bars.png")

# ── 6. Figure 4: Heatmap of GDP growth over time ─────────────
fig, ax = plt.subplots(figsize=(16, 7))
heatmap_data = GDP.loc[countries, :]
heatmap_data.index = [names[c] for c in countries]

sns.heatmap(heatmap_data, ax=ax,
            cmap="RdYlGn", center=0,
            vmin=-20, vmax=20,
            linewidths=0.3, linecolor="white",
            cbar_kws={"label": "GDP Growth Rate (%)"},
            xticklabels=5)
ax.set_title("GDP Growth Rate Heatmap — Latin America (1960–2024)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig04_heatmap.png", dpi=150,
            bbox_inches="tight")
plt.close()
print("  Saved: fig04_heatmap.png")

# ── 7. Figure 5: Individual panels for 6 most volatile ────────
top6 = vol.sort_values(ascending=False).head(6).index.tolist()
fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
axes = axes.flatten()

for i, c in enumerate(top6):
    row = GDP.loc[c].dropna()
    axes[i].plot(row.index, row.values,
                 color=PALETTE[countries.index(c)], linewidth=1.2)
    axes[i].axhline(0, color="black", linewidth=0.6,
                    linestyle="--", alpha=0.6)
    for yr in crises:
        axes[i].axvline(yr, color="red", linewidth=0.6,
                        linestyle=":", alpha=0.5)
    axes[i].set_title(f"{names[c]}  (σ={vol[c]:.1f}%)",
                      fontsize=10, fontweight="bold")
    axes[i].grid(True, alpha=0.3)
    axes[i].set_ylabel("GDP Growth (%)", fontsize=8)

fig.suptitle("Top 6 Most Volatile Economies — GDP Growth (1960–2024)",
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig05_top6_volatile.png", dpi=150)
plt.close()
print("  Saved: fig05_top6_volatile.png")

# ── 8. Figure 6: Rolling std (time-varying volatility) ────────
fig, ax = plt.subplots(figsize=(12, 5))
for i, c in enumerate(countries):
    row = GDP.loc[c].dropna()
    rolling_std = row.rolling(window=5, center=True).std()
    ax.plot(rolling_std.index, rolling_std.values,
            color=PALETTE[i], linewidth=0.8, alpha=0.6)

# Regional average rolling std
regional_roll = GDP.T.rolling(window=5, center=True).std().mean(axis=1)
ax.plot(years, regional_roll.values, color="black",
        linewidth=2.2, label="Regional Average (5-yr rolling σ)")

for yr in crises:
    ax.axvline(yr, color="red", linewidth=0.7, linestyle=":", alpha=0.6)

ax.set_title("Time-Varying Volatility — 5-Year Rolling Std Dev of GDP Growth",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Rolling Std Dev (%)", fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "fig06_rolling_volatility.png", dpi=150)
plt.close()
print("  Saved: fig06_rolling_volatility.png")

print()
print("=" * 55)
print("  Exploratory analysis complete.")
print(f"  All figures saved to: {OUTPUT_DIR}/")
print("=" * 55)