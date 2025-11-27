import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

def find_data_file(filename):
    script_dir = Path(__file__).resolve().parent
    possible_paths = [
        script_dir / filename,
        Path.cwd() / filename,
        script_dir.parent / filename,
        script_dir.parent / "council area with elec consumption" / filename,
        script_dir.parent / "clean_data" / filename,
    ]
    for path in possible_paths:
        if path.exists(): return path
    return None

def plot_urban_vs_island_trend():
    #Load Data
    filename = "Scotland_Council_Change_Analysis.csv"
    data_path = find_data_file(filename)
    
    if not data_path:
        print("Error: Data file not found.")
        return

    df = pd.read_csv(data_path, index_col=0)
    
    #Define Groups
    # Group A: Major Cities (Urban)
    urban_councils = ['Glasgow City', 'City of Edinburgh', 'Aberdeen City', 'Dundee City']
    
    # Group B: Major Islands (Rural/Off-Grid)
    island_councils = ['Orkney Islands', 'Shetland Islands', 'Na h-Eileanan Siar']
    
    #Extract Time Series Data
    years = [str(y) for y in range(2015, 2024)]
    
    # Check if names exist in dataset to avoid errors
    urban_valid = [c for c in urban_councils if c in df.index]
    island_valid = [c for c in island_councils if c in df.index]
    
    # Calculate Mean Consumption per year for each group
    urban_trend = df.loc[urban_valid, years].mean()
    island_trend = df.loc[island_valid, years].mean()
    
    # Also calculate the Scotland National Average (All 32 councils) for context
    national_trend = df[years].mean()

    #Plotting
    plt.figure(figsize=(12, 8))
    
    # Convert index to integer for plotting
    x_axis = [int(y) for y in years]
    
    # Plot Lines
    plt.plot(x_axis, island_trend, marker='o', color='#d62728', linewidth=3, label='Islands (Rural/Off-Grid)')
    plt.plot(x_axis, urban_trend, marker='s', color='#2ca02c', linewidth=3, label='Cities (Urban/High Density)')
    plt.plot(x_axis, national_trend, marker='', color='grey', linewidth=2, linestyle='--', alpha=0.6, label='Scotland Average')

    #Add "Event Windows" (Shaded Backgrounds)
    # Covid-19 Lockdown (2020)
    plt.axvspan(2019.5, 2020.5, color='gray', alpha=0.15, label='Covid-19 Lockdown')
    
    # Energy Crisis (2022)
    plt.axvspan(2021.5, 2022.5, color='orange', alpha=0.15, label='Energy Crisis Impact')

    #Annotations to tell the story
    # Annotate the "Gap"
    gap_2015 = island_trend['2015'] - urban_trend['2015']
    gap_2023 = island_trend['2023'] - urban_trend['2023']
    
    plt.annotate(f'Huge Base Load Gap\n(~{gap_2023:.0f} kWh difference)', 
                 xy=(2023, (island_trend['2023'] + urban_trend['2023'])/2), 
                 xytext=(2020.5, 5000),
                 arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2", color='black'),
                 fontsize=11, fontweight='bold', bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

    #Styling
    plt.title('Divergent Realities: Electricity Consumption Trends (2015-2023)\nUrban Cities vs. Remote Islands', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Consumption (kWh per household)', fontsize=12)
    plt.xticks(x_axis)
    plt.legend(loc='upper right', fontsize=11, frameon=True)
    plt.grid(True, linestyle='--', alpha=0.5)

    #Save
    plt.tight_layout()
    output_path = Path(__file__).resolve().parent / 'Time_Series_Comparison.png'
    plt.savefig(output_path, dpi=300)
    print(f"Chart saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_urban_vs_island_trend()