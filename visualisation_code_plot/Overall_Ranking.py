import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set plotting style to be clean and professional
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

def find_data_file(filename):
    """
    Helper function to locate the data file in various directories.
    """
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

def plot_overall_trend_ranking():
    #Locate and Load Data
    filename = "Scotland_Council_Change_Analysis.csv"
    data_path = find_data_file(filename)
    
    if not data_path:
        print(f"Error: Could not find '{filename}'. Please ensure the analysis script was run.")
        return

    df = pd.read_csv(data_path, index_col=0)
    
    #Prepare Data for Plotting
    # Sort the data: Largest reduction (most negative change) at the TOP
    df_sorted = df.sort_values(by='Change_Pct', ascending=True)
    
    # Create a color list based on the values
    # Green for reduction (negative change), Red for increase (positive change)
    colors = ['#2ca02c' if x < 0 else '#d62728' for x in df_sorted['Change_Pct']]
    
    #Create the Horizontal Bar Chart
    # Set figure height to fit all 32 council areas comfortably
    plt.figure(figsize=(12, 14))
    
    # Create the bars
    bars = plt.barh(df_sorted.index, df_sorted['Change_Pct'], color=colors, height=0.65)
    
    #Add Styling and Decorations
    plt.axvline(0, color='black', linewidth=1.2, linestyle='-') # Center line at 0%
    
    # Title and Labels using neutral terminology
    plt.title('9-Year Electricity Consumption Shift (2015 - 2023)\nRanked by Percentage Change in Scottish Council Areas', 
              fontsize=16, fontweight='bold', pad=25)
    plt.xlabel('Total Percentage Change (%)', fontsize=13)
    plt.ylabel('Council Area', fontsize=13)
    
    # Invert Y-axis so the area with Rank 1 is at the TOP
    plt.gca().invert_yaxis()
    
    # Add Gridlines (Vertical only) for easier reading
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    
    #Add Value Labels to Each Bar
    # Place percentage values inside the bars for better readability
    for bar in bars:
        width = bar.get_width() # width is negative, e.g., -24.0
        
        # Position: Inside the bar (width + offset towards 0)
        label_x_pos = width + 0.5 
        
        plt.text(label_x_pos, 
                 bar.get_y() + bar.get_height()/2, 
                 f'{width:.1f}%', 
                 va='center', 
                 ha='left',     # Left align to ensure text extends inside the bar
                 fontsize=10, 
                 fontweight='bold',
                 color='white') # White font for contrast against green bars

    
    #Highlight the largest reduction (Top of the list)
    top_saver_idx = 0
    top_val = df_sorted['Change_Pct'].iloc[top_saver_idx]
    
    plt.text(top_val, -0.9, 
             "Largest Reduction\n(Urban/High Density)", 
             ha='left', va='bottom', 
             fontweight='bold', color='#2ca02c', fontsize=11,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

    #Highlight the smallest reduction (Bottom of the list)
    worst_performer_idx = len(df_sorted) - 1
    worst_val = df_sorted['Change_Pct'].iloc[worst_performer_idx]
    
    # Position text slightly to the left to avoid overlapping with the bar end
    plt.text(worst_val - 2.5, worst_performer_idx - 0.2, 
             "Smallest Reduction\n(Island/Off-Grid)", 
             ha='right', va='center', 
             fontweight='bold', color='black', fontsize=11,
             bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1))

    #Save and Show
    plt.tight_layout()
    output_path = Path(__file__).resolve().parent / 'Overall_Ranking.png'
    plt.savefig(output_path, dpi=300)
    print(f"Chart saved successfully to: {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_overall_trend_ranking()