import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'


# --------------------------------------------------------------------
# Find CSV anywhere in project (same system as your teammate)
# --------------------------------------------------------------------
def find_data_file(filename):
    script_dir = Path(__file__).resolve().parent
    possible_paths = [
        script_dir / filename,
        script_dir.parent / filename,
        script_dir.parent / "clean_data" / filename,
        script_dir.parent / "council area with elec consumption" / filename,
        Path.cwd() / filename,
    ]
    for p in possible_paths:
        if p.exists():
            return p
    return None


# --------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------
def main():

    # ---- Load data ----
    filename = "Scotland_Council_Change_Analysis.csv"
    data_path = find_data_file(filename)

    if not data_path:
        print("CSV not found.")
        return

    df = pd.read_csv(data_path)

    # ---- List of year columns from your CSV ----
    year_cols = [str(y) for y in range(2015, 2024)]   # 2015–2023

    # Check they exist
    missing = [c for c in year_cols if c not in df.columns]
    if missing:
        print("Missing columns:", missing)
        return

    # ---- Make pivot table (rows = council, columns = years) ----
    pivot = df.set_index("Council_Area")[year_cols]

    # ---- Compute year-on-year ----
    yoy_kwh = {}
    yoy_pct = {}

    for i in range(1, len(year_cols)):
        prev = year_cols[i - 1]
        curr = year_cols[i]

        yoy_kwh[f"Change_{prev}_{curr}"] = pivot[curr] - pivot[prev]
        yoy_pct[f"Percent_{prev}_{curr}"] = (pivot[curr] - pivot[prev]) / pivot[prev] * 100

    # Add new columns
    for c in yoy_kwh:  pivot[c] = yoy_kwh[c]
    for c in yoy_pct: pivot[c] = yoy_pct[c]

    # ----------------------------------------------------------------
    # GRAPH 1 – National Average Trend (2015–2023)
    # ----------------------------------------------------------------
    save_dir = Path(__file__).resolve().parent

    scotland_avg = pivot[year_cols].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(year_cols, scotland_avg, marker='o', linewidth=2)
    plt.title("Average Electricity Consumption (2015–2023)")
    plt.xlabel("Year")
    plt.ylabel("Consumption (kWh)")
    plt.grid(True)

    out1 = save_dir / "YoY_Scotland_Average_Line.png"
    plt.savefig(out1, dpi=300, bbox_inches="tight")
    plt.close()


    # ----------------------------------------------------------------
    # GRAPH 2 – Bar chart of latest YoY change (2022 → 2023)
    # ----------------------------------------------------------------
    prev = "2022"
    curr = "2023"
    col = f"Percent_{prev}_{curr}"

    if col in pivot.columns:
        bar_data = pivot[col].sort_values(ascending=False)

        plt.figure(figsize=(12, 8))
        plt.bar(bar_data.index, bar_data.values)
        plt.xticks(rotation=90)
        plt.title(f"Percentage Change {prev} to {curr}")
        plt.ylabel("% Change")

        out2 = save_dir / f"YoY_Change_{prev}_to_{curr}.png"
        plt.savefig(out2, dpi=300, bbox_inches="tight")
        plt.close()
    else:
        print(f"Column {col} not found — bar chart skipped.")


    print("\nSaved:")
    print(" -", out1)
    if col in pivot.columns:
        print(" -", out2)


# Run script
if __name__ == "__main__":
    main()
