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

def plot_shock_correlation():
    filename = "Scotland_Council_Change_Analysis.csv"
    data_path = find_data_file(filename)
    
    if not data_path:
        print("Error: Data file not found.")
        return

    try:
        df = pd.read_csv(data_path, index_col=0)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Recalculate metrics
    df['Covid_Impact'] = ((df['2020'] - df['2019']) / df['2019']) * 100
    df['Crisis_Impact'] = ((df['2022'] - df['2021']) / df['2021']) * 100

    plt.figure(figsize=(14, 11)) # Larger figure size to accommodate text labels
    
    # Plotting
    scatter = plt.scatter(df['Covid_Impact'], df['Crisis_Impact'], 
                          c=df['Crisis_Impact'], cmap='RdYlGn_r', 
                          s=130, edgecolors='grey', alpha=0.9)

    # Reference lines
    plt.axhline(0, color='black', linewidth=1, linestyle='--')
    plt.axvline(0, color='black', linewidth=1, linestyle='--')
    
    mean_covid = df['Covid_Impact'].mean()
    mean_crisis = df['Crisis_Impact'].mean()
    plt.axvline(mean_covid, color='blue', linestyle=':', alpha=0.6, label=f'Avg Covid Impact (+{mean_covid:.1f}%)')
    plt.axhline(mean_crisis, color='red', linestyle=':', alpha=0.6, label=f'Avg Crisis Impact ({mean_crisis:.1f}%)')

    # Legend
    plt.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=10)

    # Label all data points
    try:
        from adjustText import adjust_text
        texts = []
        # Iterate through all council areas
        for council in df.index:
            # Ensure data is not NaN before plotting
            if pd.notna(df.loc[council, 'Covid_Impact']) and pd.notna(df.loc[council, 'Crisis_Impact']):
                texts.append(plt.text(df.loc[council, 'Covid_Impact'], 
                                      df.loc[council, 'Crisis_Impact'], 
                                      council, 
                                      fontsize=8, 
                                      fontweight='semibold',
                                      alpha=0.9))
        
        # Call auto-adjust position for labels
        print("Calculating text positions, please wait...")
        adjust_text(texts, arrowprops=dict(arrowstyle='-', color='grey', lw=0.5))
        
    except ImportError:
        print("Warning: adjustText not installed, labels will overlap significantly! Please pip install adjustText")
        for council in df.index:
            plt.text(df.loc[council, 'Covid_Impact'], df.loc[council, 'Crisis_Impact'], council, fontsize=8)

    # Titles and labels
    plt.title('External Shocks Analysis: Covid-19 (Lockdown) vs Energy Crisis (Price)\nHow did different Scottish areas react?', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Covid-19 Impact (2019->2020)\n% Increase in Consumption (Stay at Home)', fontsize=12)
    plt.ylabel('Energy Crisis Impact (2021->2022)\n% Decrease in Consumption (Price Hike)', fontsize=12)
    
    plt.colorbar(scatter, label='Crisis Impact Magnitude')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Axis limits
    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()
    
    # Top-right annotation box
    plt.text(x_max*0.98, y_max*0.98, 
             "Rigid Demand\n(Islands/Rural)\n\nLow Price Sensitivity", 
             ha='right', va='top', color='#d62728', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9, edgecolor='#d62728'))
    
    # Bottom-left annotation box
    x_pos = x_min + (x_max - x_min) * 0.03 
    y_pos = y_min + (y_max - y_min) * 0.03
    
    plt.text(x_pos, y_pos, 
             "High Elasticity\n(Cities/Suburbs)\n\nHigh Price Sensitivity", 
             ha='left', va='bottom', color='#2ca02c', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9, edgecolor="#2ca02c"))

    plt.tight_layout()
    output_path = Path(__file__).resolve().parent / 'The _Shock Correlation_Scatter_Plot.png'
    plt.savefig(output_path, dpi=300)
    print(f"Full labeled chart saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_shock_correlation()