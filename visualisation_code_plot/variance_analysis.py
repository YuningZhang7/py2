import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'



# Function: Find dataset

def find_data_file(filename):
    script_dir = Path(__file__).resolve().parent
    possible_paths = [
        script_dir / filename,
        script_dir.parent / filename,
        script_dir.parent / "clean data" / filename,
        script_dir.parent / "council area with elec consumption" / filename,
    ]
    for path in possible_paths:
        if path.exists():
            return path
    return None

def main():
    filename = "Scotland_Council_Change_Analysis.csv"
    data_path = find_data_file(filename)

    if not data_path:
        print("Error: Could not locate the file.")
        return

    # Load CSV
    df = pd.read_csv(data_path)


    # Step 1: Extract only year columns automatically

    year_cols = [col for col in df.columns if col.isdigit()]

    if not year_cols:
        print("Error: No year columns found.")
        return


    # Step 2: Compute variance for each council

    df["Variance"] = df[year_cols].var(axis=1)

    print("\nTop councils by variance:\n")
    print(df[["Council_Area", "Variance"]].sort_values("Variance", ascending=False).head(10))

    # Step 3: Create output folder
 
    save_dir = Path(__file__).resolve().parent


    # Step 4: Plot variance bar chart
    df_sorted = df.sort_values("Variance", ascending=False)

    plt.figure(figsize=(14, 8))
    plt.bar(df_sorted["Council_Area"], df_sorted["Variance"])
    plt.xticks(rotation=90)
    plt.xlabel("Council Area")
    plt.ylabel("Variance in Electricity Consumption")
    plt.title("Variance of Electricity Consumption by Council (2015–2023)")
    plt.tight_layout()

    # Save graph
    bar_chart_path = save_dir / "Variance_Analysis.png"
    plt.savefig(bar_chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nVariance chart saved to: {bar_chart_path}\n")


if __name__ == "__main__":
    main()
