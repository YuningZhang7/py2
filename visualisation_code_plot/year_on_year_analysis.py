import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'



# Find CSV anywhere in project

def find_data_file(filename):
    script_dir = Path(__file__).resolve().parent
    possible_paths = [
        script_dir / filename,
        script_dir.parent / filename,
        script_dir.parent / "clean_data" / filename,
        script_dir.parent / "council area with elec consumption" / filename,
        Path.cwd() / filename,
    ]
    # We loop through all possible paths and return the one that exists.
    for p in possible_paths:
        if p.exists():     # if the file we want exists at this path
            return p
    return None


def main():

    # Load data
    filename = "Scotland_Council_Change_Analysis.csv"
    data_path = find_data_file(filename)  # Search for csv

    if not data_path:
        print("CSV not found.")
        return

    df = pd.read_csv(data_path)           # Load my csv into pandas dataframe.

    # List of year columns from your CSV
    year_cols = [str(y) for y in range(2015, 2024)]   # 2015–2023, convert numbers to strings

    # Check they exist
    missing = [c for c in year_cols if c not in df.columns]
    if missing:
        print("Missing columns:", missing) # showing if any year columns are missings
        return

    # Make pivot table (rows = council, columns = years)
    pivot = df.set_index("Council_Area")[year_cols]

    # Compute year-on-year
    yoy_kwh = {}     # Dictionary for absolute change (kWh)
    yoy_pct = {}     # Dictionary for percent change (%)

    for i in range(1, len(year_cols)):
        prev = year_cols[i - 1]  # Calculation for previous year 
        curr = year_cols[i]      # Calculation for current year

        # We now compute the absolute change between years
        yoy_kwh[f"Change_{prev}_{curr}"] = pivot[curr] - pivot[prev]
        # then, we compute percentage change
        yoy_pct[f"Percent_{prev}_{curr}"] = (pivot[curr] - pivot[prev]) / pivot[prev] * 100

    # Add new columns, add YoY results back into pivot table
    for c in yoy_kwh:  pivot[c] = yoy_kwh[c]
    for c in yoy_pct: pivot[c] = yoy_pct[c]

    
    # GRAPH 1 – National Average Trend (2015–2023)

    save_dir = Path(__file__).resolve().parent

    scotland_avg = pivot[year_cols].mean()

    plt.figure(figsize=(10, 6)) # Define plot size
    plt.plot(year_cols, scotland_avg, marker='o', linewidth=2) # Draw line chart
    plt.title("Average Electricity Consumption (2015–2023)")
    plt.xlabel("Year")
    plt.ylabel("Consumption (kWh)")
    plt.grid(True)

    out1 = save_dir / "YoY_Scotland_Average_Line.png"
    plt.savefig(out1, dpi=300, bbox_inches="tight")
    plt.close()


    
    # GRAPH 2 – Bar chart of latest YoY change (2022 → 2023)

    prev = "2022" # Previous year
    curr = "2023" # Current year
    col = f"Percent_{prev}_{curr}"  # Column name for percent change

    if col in pivot.columns:
        bar_data = pivot[col].sort_values(ascending=False)

        plt.figure(figsize=(12, 8))
        plt.bar(bar_data.index, bar_data.values) # Plot bar chart
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
