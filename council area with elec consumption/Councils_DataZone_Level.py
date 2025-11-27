import pandas as pd
from pathlib import Path

#CONFIGURATION
TARGET_COUNCILS = [
    "Glasgow City", 
    "City of Edinburgh", 
    "Orkney Islands", 
    "Highland", 
    "West Lothian"
]

OUTPUT_FILE = "Selected_5_Councils_DataZone_Level.csv"


# Mapping GSS Council Codes to readable names
COUNCIL_MAPPING = {
    "S12000033": "Aberdeen City", "S12000034": "Aberdeenshire", "S12000041": "Angus",
    "S12000035": "Argyll and Bute", "S12000036": "City of Edinburgh", "S12000005": "Clackmannanshire",
    "S12000006": "Dumfries and Galloway", "S12000042": "Dundee City", "S12000008": "East Ayrshire",
    "S12000045": "East Dunbartonshire", "S12000010": "East Lothian", "S12000011": "East Renfrewshire",
    "S12000014": "Falkirk", "S12000047": "Fife", "S12000049": "Glasgow City",
    "S12000017": "Highland", "S12000018": "Inverclyde", "S12000019": "Midlothian",
    "S12000020": "Moray", "S12000013": "Na h-Eileanan Siar", "S12000021": "North Ayrshire",
    "S12000050": "North Lanarkshire", "S12000023": "Orkney Islands", "S12000048": "Perth and Kinross",
    "S12000038": "Renfrewshire", "S12000026": "Scottish Borders", "S12000027": "Shetland Islands",
    "S12000028": "South Ayrshire", "S12000029": "South Lanarkshire", "S12000030": "Stirling",
    "S12000039": "West Dunbartonshire", "S12000040": "West Lothian"
}

#HELPER FUNCTION
def find_file(filename):
    """
    Search for files in standard project directories.
    """
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    # Define potential paths including specific data directories
    specific_path = project_root / "cleaning data with code" / "clean_data" / filename
    
    possible_paths = [
        specific_path,
        script_dir / filename,
        script_dir / "clean_data" / filename,
        Path.cwd() / "clean_data" / filename,
        project_root / "clean_data" / filename,
    ]
    
    # Check specific paths first
    for path in possible_paths:
        if path.exists(): return path
            
    # Recursive search as fallback
    try:
        results = list(project_root.rglob(filename))
        if results: return results[0]
    except:
        pass

    return None

def process_datazone_aggregation():
    print("Starting Data Zone Level Extraction")
    
    #Load Scottish Postcode Lookup (SSPL)
    sspl_file = find_file("Scottish_Postcode_Lookup_2025_1.csv")
    if not sspl_file:
        print("CRITICAL: SSPL file not found.")
        return

    print(f"Loading SSPL: {sspl_file.name}")
    try:
        # Determine column names dynamically or use defaults
        header = pd.read_csv(sspl_file, nrows=0).columns.tolist()
        pc_col = next((c for c in header if "postcode" in c.lower().replace(" ", "")), "Postcode")
        council_code_col = "CouncilArea2019Code"
        dz_code_col = "DataZone2022Code"
        
        # Read only necessary columns
        sspl = pd.read_csv(sspl_file, usecols=[pc_col, council_code_col, dz_code_col], low_memory=False)
        sspl = sspl.rename(columns={pc_col: 'Postcode', council_code_col: 'Council_Code', dz_code_col: 'DataZone'})
        
        # Map Council Codes to Names for filtering
        sspl['Council_Area'] = sspl['Council_Code'].map(COUNCIL_MAPPING)
        sspl['Postcode'] = sspl['Postcode'].astype(str).str.replace(" ", "").str.upper()
    except Exception as e:
        print(f"SSPL Error: {e}")
        return

    #Filter SSPL for Target Councils
    sspl_filtered = sspl[sspl['Council_Area'].isin(TARGET_COUNCILS)].copy()
    print(f"Filtered SSPL: {len(sspl_filtered)} rows for target councils.")
    
    all_years_data = []

    #Process Yearly Electricity Data (2015-2023)
    for year in range(2015, 2024):
        elec_filename = f"electricity_scotland_{year}.csv"
        elec_path = find_file(elec_filename)
        
        if not elec_path:
            print(f"[{year}] File not found: {elec_filename}")
            continue
            
        print(f"[{year}] Processing: {elec_path.name}")
        
        try:
            df_elec = pd.read_csv(elec_path)
            # Clean column headers
            df_elec.columns = [c.strip() for c in df_elec.columns]
            
            # Dynamic Column Identification
            # 1. Postcode
            pc_col_elec = next((c for c in df_elec.columns if 'post' in c.lower()), None)
            
            # 2. Total Consumption (contains 'cons' or 'kwh', exclude mean/median)
            total_col = next((c for c in df_elec.columns if ('cons' in c.lower() or 'kwh' in c.lower()) and 'mean' not in c.lower() and 'median' not in c.lower()), None)
            
            # 3. Number of Meters
            meters_col = next((c for c in df_elec.columns if 'meter' in c.lower() or 'num' in c.lower()), None)
            
            if not (pc_col_elec and total_col and meters_col):
                print(f"  [SKIP] Could not identify required columns in {year}.")
                continue
                
            # Data Cleaning
            df_elec['Postcode'] = df_elec[pc_col_elec].astype(str).str.replace(" ", "").str.upper()
            df_elec[total_col] = pd.to_numeric(df_elec[total_col], errors='coerce').fillna(0)
            df_elec[meters_col] = pd.to_numeric(df_elec[meters_col], errors='coerce').fillna(0)
            
            # Merge Electricity Data with SSPL (DataZone info)
            merged = pd.merge(df_elec, sspl_filtered, on='Postcode', how='inner')
            
            if merged.empty:
                print(f"  [WARN] Merged 0 rows.")
                continue
            
            # Aggregate from Postcode level to DataZone level
            dz_stats = merged.groupby(['Council_Area', 'DataZone'])[[total_col, meters_col]].sum().reset_index()
            
            # Calculate Mean Consumption per DataZone
            dz_stats['Mean_Consumption_kWh'] = dz_stats[total_col] / dz_stats[meters_col]
            dz_stats['Year'] = year
            
            print(f"  -> Extracted data for {len(dz_stats)} DataZones.")
            all_years_data.append(dz_stats)
            
        except Exception as e:
            print(f"  [ERROR] {e}")
            continue

    #Save Final Dataset
    if not all_years_data:
        print("\nNo data collected.")
        return
        
    final_df = pd.concat(all_years_data, ignore_index=True)
    final_df = final_df.sort_values(by=['Council_Area', 'DataZone', 'Year'])
    
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSuccess! Saved {len(final_df)} rows to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_datazone_aggregation()