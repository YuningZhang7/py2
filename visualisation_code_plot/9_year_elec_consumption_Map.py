import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from adjustText import adjust_text
import warnings

# Suppress specific warnings from adjustText regarding arrow patches to keep the output clean
warnings.filterwarnings("ignore", message=".*FancyArrowPatch.*")

#CONFIGURATION
# Input data file generated from the analysis phase
DATA_FILE = "Scotland_Council_Change_Analysis.csv"
# Official GeoJSON source for Scottish Local Authority Districts (LAD)
GEOJSON_URL = "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/sco/lad.json"

#HELPER FUNCTION
def find_data_file(filename):
    """
    Locate the input file recursively. 
    This ensures the script runs correctly regardless of the current working directory.
    """
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    # Priority search paths
    possible_paths = [
        script_dir / filename,
        Path.cwd() / filename,
        project_root / filename,
        project_root / "council area with elec consumption" / filename
    ]
    
    for path in possible_paths:
        if path.exists(): return path
            
    # Fallback: Search entire project directory
    try:
        results = list(project_root.rglob(filename))
        if results: return results[0]
    except Exception:
        pass

    return None

def plot_scotland_map_final():
    """
    Generates a high-resolution choropleth map of Scotland showing 9-year electricity consumption trends.
    Uses strict auto-cropping and dynamic aspect ratio calculation to maximize map size.
    """
    print("Generating Final 9-Year Trend Visualization")

    # 1. Load Statistical Data
    csv_path = find_data_file(DATA_FILE)
    if not csv_path: 
        print(f"Error: {DATA_FILE} not found. Please run the analysis script first.")
        return
    df = pd.read_csv(csv_path, index_col=0)

    # 2. Load Geographical Data (GeoJSON)
    try:
        gdf = gpd.read_file(GEOJSON_URL)
    except Exception as e:
        print(f"Error downloading map data: {e}")
        return

    #Data Cleaning: Name Standardization
    name_corrections = {
        "Edinburgh, City of": "City of Edinburgh", "Glasgow City": "Glasgow City",
        "Aberdeen City": "Aberdeen City", "Dundee City": "Dundee City",
        "Eilean Siar": "Na h-Eileanan Siar", "Orkney Islands": "Orkney Islands",
        "Shetland Islands": "Shetland Islands", "Highland": "Highland",
        "Argyll and Bute": "Argyll and Bute", "Moray": "Moray",
        "Aberdeenshire": "Aberdeenshire", "Stirling": "Stirling",
        "Falkirk": "Falkirk", "Clackmannanshire": "Clackmannanshire",
        "Fife": "Fife", "West Lothian": "West Lothian", "Midlothian": "Midlothian",
        "East Lothian": "East Lothian", "Scottish Borders": "Scottish Borders",
        "Dumfries and Galloway": "Dumfries and Galloway", "South Ayrshire": "South Ayrshire",
        "East Ayrshire": "East Ayrshire", "North Ayrshire": "North Ayrshire",
        "South Lanarkshire": "South Lanarkshire", "North Lanarkshire": "North Lanarkshire",
        "East Dunbartonshire": "East Dunbartonshire", "West Dunbartonshire": "West Dunbartonshire",
        "Renfrewshire": "Renfrewshire", "East Renfrewshire": "East Renfrewshire",
        "Inverclyde": "Inverclyde", "Angus": "Angus", "Perth and Kinross": "Perth and Kinross"
    }
    gdf['Council_Area'] = gdf['LAD13NM'].replace(name_corrections)

    #Merge Data
    merged_map = gdf.merge(df, left_on='Council_Area', right_index=True, how='left')

    #DYNAMIC ASPECT RATIO CALCULATION
    # Get strict geographical bounds
    minx, miny, maxx, maxy = merged_map.total_bounds
    
    geo_width = maxx - minx
    geo_height = maxy - miny
    
    # Increase base width to 20 inches to make the map dominant
    fig_width = 20
    fig_height = fig_width * (geo_height / geo_width)
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
    
    #STRICT ZOOM LIMITS 
    # Set axis limits exactly to the bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    #Draw the Choropleth Map
    # cmap='RdYlGn_r': Negative values (Reduction) = Green; Positive/High values = Red.
    merged_map.plot(column='Change_Pct', 
                    ax=ax, 
                    cmap='RdYlGn_r', 
                    edgecolor='black', 
                    linewidth=0.5)

    # Add Colorbar
    sm = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=plt.Normalize(vmin=merged_map['Change_Pct'].min(), vmax=merged_map['Change_Pct'].max()))
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, shrink=0.4, aspect=35, pad=0.01, location='bottom')
    cbar.set_label("9-Year Change in Electricity Consumption (%)", fontsize=14)

    # Styling
    ax.axis('off') # Hide latitude/longitude axes
    plt.title('Geographic Disparity in Energy Trends (2015-2023)\nAll Council Areas Labeled', 
              fontsize=24, fontweight='bold', pad=30)

    #Advanced Labeling with Collision Avoidance
    print("Optimizing label positions")
    texts = []
    
    for idx, row in merged_map.iterrows():
        if pd.isna(row['Change_Pct']): continue
        
        # Determine label coordinates
        x, y = row.geometry.centroid.x, row.geometry.centroid.y
        
        # Clean up names for display
        name = row['Council_Area'].replace("City of ", "").replace(" Islands", "").replace("Na h-", "")
        label_text = f"{name}\n{row['Change_Pct']:.1f}%"
        
        # Create text object with a translucent bounding box
        texts.append(ax.text(x, y, label_text, 
                             fontsize=10, 
                             fontweight='bold', 
                             ha='center', 
                             color='black',
                             bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.6, ec='none')))

    # Use adjust_text to repel labels from each other and draw leader lines
    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color='black', lw=0.5),
                expand_points=(1.2, 1.2),
                force_text=(0.3, 0.5),
                lim=100)

    #Output with tight layout
    output_path = Path(__file__).resolve().parent / '9_year_elec_consumption_Map.png'
    # bbox_inches='tight' removes any remaining whitespace
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Map saved successfully to: {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_scotland_map_final()