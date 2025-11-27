import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from adjustText import adjust_text
import warnings

# Suppress warnings related to arrow patches in adjustText for a cleaner output log
warnings.filterwarnings("ignore", message=".*FancyArrowPatch.*")

#CONFIGURATION
# Input data file generated from the previous analysis phase
DATA_FILE = "Scotland_Council_Change_Analysis.csv"
# Official GeoJSON source for Scottish Local Authority Districts
GEOJSON_URL = "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/sco/lad.json"

#HELPER FUNCTION
def find_data_file(filename):
    """
    Robust file finder that searches project directories recursively.
    This ensures the script runs correctly regardless of the current working directory.
    """
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    # Define priority search paths
    possible_paths = [
        script_dir / filename,
        Path.cwd() / filename,
        project_root / filename,
        project_root / "council area with elec consumption" / filename
    ]
    
    for path in possible_paths:
        if path.exists(): return path
            
    # Fallback: Recursive search in the project root
    try:
        results = list(project_root.rglob(filename))
        if results: return results[0]
    except Exception:
        pass

    return None

def generate_zoomed_map(gdf, df, target_col, title, output_filename, color_label):
    """
    Generates a high-resolution, cropped choropleth map.
    
    Key Features:
     Dynamic Aspect Ratio: Calculates figure size based on geographic bounds to eliminate whitespace.
     Strict Cropping: Zooms in specifically on the landmass.
    """
    print(f"Generating optimized map: {output_filename} ...")
    
    # Merge Statistical Data with Geographical Data
    merged_map = gdf.merge(df, left_on='Council_Area', right_index=True, how='left')

    #DYNAMIC ASPECT RATIO CALCULATION
    # Get the strict geographical bounds of the data
    minx, miny, maxx, maxy = merged_map.total_bounds
    
    geo_width = maxx - minx
    geo_height = maxy - miny
    
    # Set a base width (in inches) large enough for clear text rendering
    fig_width = 20
    # Calculate height to match the map's natural aspect ratio
    fig_height = fig_width * (geo_height / geo_width)
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
    
    #STRICT ZOOM LIMITS
    # Set axis limits exactly to the bounds to crop out excess ocean
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    # Plot the Choropleth Map
    # Colormap 'RdYlGn_r': Red (High Increase/Bad) <-> Green (Decrease/Good)
    merged_map.plot(column=target_col, 
                    ax=ax, 
                    cmap='RdYlGn_r', 
                    edgecolor='black', 
                    linewidth=0.5)

    # Configure Colorbar
    sm = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=plt.Normalize(vmin=merged_map[target_col].min(), vmax=merged_map[target_col].max()))
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, shrink=0.4, aspect=35, pad=0.01, location='bottom')
    cbar.set_label(color_label, fontsize=14)

    # Styling
    ax.axis('off')
    plt.title(title, fontsize=24, fontweight='bold', pad=30)

    # Labeling Logic
    texts = []
    for idx, row in merged_map.iterrows():
        if pd.isna(row[target_col]): continue
        
        # Calculate centroid for label placement
        x, y = row.geometry.centroid.x, row.geometry.centroid.y
        
        # Clean up names for better display
        name = row['Council_Area'].replace("City of ", "").replace(" Islands", "").replace("Na h-", "")
        
        label_text = f"{name}\n{row[target_col]:+.1f}%"
        
        # Add text with a semi-transparent white box for readability against map colors
        texts.append(ax.text(x, y, label_text, 
                             fontsize=10, 
                             fontweight='bold', 
                             ha='center', 
                             color='black',
                             bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.6, ec='none')))

    # Optimize label placement using physics simulation
    print(f"  -> Optimizing labels for {output_filename}...")
    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color='black', lw=0.5),
                expand_points=(1.2, 1.2),
                force_text=(0.3, 0.5),
                lim=100)

    # Save output
    output_path = Path(__file__).resolve().parent / output_filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  -> Saved to: {output_path}")
    plt.close()

def process_event_maps():
    #Load Data
    csv_path = find_data_file(DATA_FILE)
    if not csv_path: 
        print(f"Error: {DATA_FILE} not found.")
        return
    df = pd.read_csv(csv_path, index_col=0)

    #Load Map GeoJSON
    try:
        gdf = gpd.read_file(GEOJSON_URL)
    except Exception as e:
        print(f"Map download error: {e}")
        return

    #Name Standardization
    # Align GeoJSON names (LAD13NM) with our Dataset names (Council Area)
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

    #Calculate Event-Specific Metrics
    
    # Scenario A: Covid Impact (2019 -> 2020)
    # Focus: Percentage Increase due to lockdowns
    df['Covid_Impact'] = ((df['2020'] - df['2019']) / df['2019']) * 100
    
    # Scenario B: Energy Crisis Impact (2021 -> 2022)
    # Focus: Percentage Decrease due to price hikes
    df['Crisis_Impact'] = ((df['2022'] - df['2021']) / df['2021']) * 100

    #Generate Maps
    generate_zoomed_map(
        gdf, df, 
        target_col='Covid_Impact',
        title='Impact of COVID-19 Lockdown (2019-2020)\n% Increase in Domestic Electricity Consumption',
        output_filename='Map_Covid_Impact.png',
        color_label='Percentage Change (2019-2020)'
    )

    generate_zoomed_map(
        gdf, df, 
        target_col='Crisis_Impact',
        title='Impact of Energy Crisis & Price Hikes (2021-2022)\n% Reduction in Domestic Electricity Consumption',
        output_filename='Map_Crisis_Impact.png',
        color_label='Percentage Change (2021-2022)'
    )

if __name__ == "__main__":
    process_event_maps()