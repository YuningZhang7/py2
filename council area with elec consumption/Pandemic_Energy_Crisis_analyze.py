import pandas as pd
from pathlib import Path

# Configuration for file names
INPUT_FILE = "Scotland_Council_Change_Analysis.csv"

# Output file names
OUTPUT_COVID = "Ranking_Covid_Impact.csv"
OUTPUT_CRISIS = "Ranking_Energy_Crisis_Impact.csv"

def generate_dual_rankings():
    #Load Data
    if not Path(INPUT_FILE).exists():
        print(f"Error: Could not find file {INPUT_FILE}. Please run the previous analysis script first.")
        return

    df = pd.read_csv(INPUT_FILE, index_col=0)
    
    # Calculate Key Metrics
    #Covid Impact (2019 -> 2020): We focus on "Percentage Increase"
    # Logic: Lockdowns forced people to stay home, increasing domestic electricity use.
    # A higher positive percentage indicates a stronger impact from the lockdown.
    df['Covid_Impact_Pct'] = ((df['2020'] - df['2019']) / df['2019']) * 100

    #Energy Crisis Impact (2021 -> 2022): We focus on "Percentage Decrease"
    # Logic: Skyrocketing prices forced households to reduce consumption.
    # A more negative percentage (larger drop) indicates a stronger impact from the price crisis.
    df['Crisis_Impact_Pct'] = ((df['2022'] - df['2021']) / df['2021']) * 100

    #Generate Two Independent Ranking Tables
    
    #Ranking 1: Pandemic Lockdown Impact
    # Sort by highest increase first
    covid_rank = df[['2019', '2020', 'Covid_Impact_Pct']].sort_values(by='Covid_Impact_Pct', ascending=False)
    covid_rank.insert(0, 'Rank', range(1, len(covid_rank) + 1)) # Add a Rank column

    #Ranking 2: Energy Crisis Impact
    # Sort by largest decrease (most negative value) first
    crisis_rank = df[['2021', '2022', 'Crisis_Impact_Pct']].sort_values(by='Crisis_Impact_Pct', ascending=True)
    crisis_rank.insert(0, 'Rank', range(1, len(crisis_rank) + 1)) # Add a Rank column

    # 4. Print Results to Terminal
    
    # Set pandas display options for better readability
    pd.set_option('display.max_rows', None)
    pd.set_option('display.float_format', '{:,.2f}%'.format)

    print("\n" + "—"*70)
    print("【 Ranking 1: Covid-19 Pandemic Impact (2019 -> 2020) 】")
    print("Ordered by: Largest INCREASE in consumption (Highest impact of lockdown)")
    print("—"*70)
    print(covid_rank[['Rank', 'Covid_Impact_Pct']])
    
    print("\n" + "—"*70)
    print("【 Ranking 2: Energy Crisis Impact (2021 -> 2022) 】")
    print("Ordered by: Largest DECREASE in consumption (Highest impact of price hike)")
    print("—"*70)
    print(crisis_rank[['Rank', 'Crisis_Impact_Pct']])

    # 5. Save Results to CSV
    covid_rank.to_csv(OUTPUT_COVID)
    crisis_rank.to_csv(OUTPUT_CRISIS)
    print(f"\nSuccessfully generated two ranking files:")
    print(f"1. {OUTPUT_COVID}")
    print(f"2. {OUTPUT_CRISIS}")

if __name__ == "__main__":
    generate_dual_rankings()