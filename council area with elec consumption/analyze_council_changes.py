"""
This script performs the core analysis of electricity consumption trends 
across Scottish Council Areas from 2015 to 2023.

It handles the entire pipeline:
1.  Locating input data (cleaned CSVs) and reference data (SSPL) intelligently.
2.  Downloading missing reference files (SSPL) automatically.
3.  Merging electricity meter data with administrative boundaries.
4.  Calculating absolute and percentage changes in consumption.
5.  Generating a ranked report csv file.

"""

import io
import sys
import zipfile
import requests
import pandas as pd
from pathlib import Path

#CONFIGURATION AND CONSTANTS

# Determine the directory where this script is currently located
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent 

# Input folder name and Reference filename
DATA_DIR_NAME = "clean_data"
SSPL_FILENAME = "Scottish_Postcode_Lookup_2025_1.csv"
SSPL_URL = "https://www.nrscotland.gov.uk/media/3zjlgpt3/sspl_2025_1.zip"

# [MODIFIED]: Output file path is now strictly forced to be in the SCRIPT_DIR
OUTPUT_FILE = SCRIPT_DIR / "Scotland_Council_Change_Analysis.csv"

# Define a list of paths to search for data
SEARCH_PATHS = [
    SCRIPT_DIR,                 
    PROJECT_ROOT,   
    PROJECT_ROOT / "cleaning data with code",
    Path.cwd()
]

#UTILITY FUNCTIONS

def find_path_smart(target_name: str, is_dir: bool = False) -> Path | None:
    """
    Locates a file or directory by searching through predefined paths.

    Args:
    target_name (str): The name of the file or directory to find.
    is_dir (bool): Set to True if searching for a directory, False for a file.

    Returns:
    Path | None: The absolute path if found, otherwise None.
    """
    for base_path in SEARCH_PATHS:
        candidate = base_path / target_name
        if candidate.exists():
            if is_dir and candidate.is_dir(): return candidate
            elif not is_dir and candidate.is_file(): return candidate
    
    # Fallback recursive search in the project root
    if is_dir:
        found = list(PROJECT_ROOT.rglob(target_name))
        for path in found:
            if path.is_dir(): return path
    else:
        found = list(PROJECT_ROOT.rglob(target_name))
        for path in found:
            if path.is_file(): return path     
            
    return None


def download_and_extract_sspl() -> Path | None:
    """
    Downloads the SSPL ZIP archive and extracts the CSV to the SCRIPT DIRECTORY.
    
    Returns:
    Path | None: Path to the extracted CSV file, or None if failed.
    """
    print(f"SSPL file missing. Downloading from official source")
    try:
        response = requests.get(SSPL_URL, stream=True)
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # Identify the CSV file within the zip
            csv_filename = next(
                (f for f in zip_ref.namelist() if f.lower().endswith(".csv") and "__MACOSX" not in f), 
                None
            )
            
            if csv_filename:
                #Extract to SCRIPT_DIR instead of PROJECT_ROOT
                zip_ref.extract(csv_filename, SCRIPT_DIR)
                
                extracted_path = SCRIPT_DIR / Path(csv_filename).name
                target_path = SCRIPT_DIR / SSPL_FILENAME
                
                if extracted_path != target_path:
                    extracted_path.rename(target_path)
                
                return target_path
            
    except Exception as e:
        print(f"Error during download/extraction: {e}")
        return None
        
    return None


def get_council_mapping() -> dict[str, str]:
    """
    Returns a dictionary mapping GSS Council Codes to readable Council Names.
    """
    return {
        "S12000005": "Clackmannanshire", "S12000006": "Dumfries and Galloway", "S12000008": "East Ayrshire",
        "S12000010": "East Lothian", "S12000011": "East Renfrewshire", "S12000013": "Na h-Eileanan Siar",
        "S12000014": "Falkirk", "S12000017": "Highland", "S12000018": "Inverclyde", "S12000019": "Midlothian",
        "S12000020": "Moray", "S12000021": "North Ayrshire", "S12000023": "Orkney Islands",
        "S12000026": "Scottish Borders", "S12000027": "Shetland Islands", "S12000028": "South Ayrshire",
        "S12000029": "South Lanarkshire", "S12000030": "Stirling",
        "S12000033": "Aberdeen City", "S12000034": "Aberdeenshire", "S12000035": "Argyll and Bute",
        "S12000036": "City of Edinburgh", "S12000038": "Renfrewshire", "S12000039": "West Dunbartonshire",
        "S12000040": "West Lothian", "S12000041": "Angus", "S12000042": "Dundee City",
        "S12000045": "East Dunbartonshire", "S12000047": "Fife", "S12000048": "Perth and Kinross",
        "S12000049": "Glasgow City", "S12000050": "North Lanarkshire"
    }

# 3. MAIN ANALYSIS LOGIC

def main():
    """
    Main execution entry point.
    """
    print("\nScotland Electricity Consumption Analysis (2015-2023)")

    #Locate Input Data
    clean_data_dir = find_path_smart(DATA_DIR_NAME, is_dir=True)
    if not clean_data_dir:
        print(f"Critical Error: Directory '{DATA_DIR_NAME}' not found.")
        print("Please run the data cleaning script first.")
        sys.exit(1)

    #Locate Reference Data (SSPL)
    sspl_path = find_path_smart(SSPL_FILENAME, is_dir=False)
    if not sspl_path:
        sspl_path = download_and_extract_sspl()
        if not sspl_path: 
            sys.exit(1)

    #Load and Prepare Reference Data
    try:
        # Read first row to dynamically detect column names
        preview_df = pd.read_csv(sspl_path, nrows=1)
        
        postcode_col = next((c for c in preview_df.columns if 'postcode' in c.lower()), 'Postcode')
        council_code_col = next((c for c in preview_df.columns if 'council' in c.lower() and 'code' in c.lower()), 'CouncilArea2019Code')
        
        sspl_df = pd.read_csv(sspl_path, usecols=[postcode_col, council_code_col], dtype=str, low_memory=False)
        
        sspl_df.rename(columns={postcode_col: 'Postcode', council_code_col: 'Council_Code'}, inplace=True)
        sspl_df['Postcode'] = sspl_df['Postcode'].str.replace(" ", "").str.upper()
        
    except Exception as e:
        print(f"Error reading SSPL file: {e}")
        sys.exit(1)

    mapping_dict = get_council_mapping()
    yearly_aggregates = []

    #Process Yearly Electricity Data ---
    print("Processing yearly data", end=" ", flush=True)
    
    for year in range(2015, 2024):
        file_path = clean_data_dir / f"electricity_scotland_{year}.csv"
        if not file_path.exists(): 
            continue
            
        try:
            elec_df = pd.read_csv(file_path)
            elec_df.columns = [c.strip() for c in elec_df.columns]
            
            #Standardize Postcode
            pc_col_data = next((c for c in elec_df.columns if c.lower() == 'postcode'), None)
            if not pc_col_data: continue
            elec_df['Postcode'] = elec_df[pc_col_data].astype(str).str.replace(" ", "").str.upper()
            
            #Identify Consumption
            mean_col = next((c for c in elec_df.columns if 'mean' in c.lower() and 'cons' in c.lower()), None)
            
            if mean_col:
                elec_df['Target_Value'] = pd.to_numeric(elec_df[mean_col], errors='coerce')
            else:
                total_col = next((c for c in elec_df.columns if 'total' in c.lower() and 'cons' in c.lower()), None)
                num_col = next((c for c in elec_df.columns if 'num' in c.lower() and 'meter' in c.lower()), None)
                if total_col and num_col:
                    elec_df['Target_Value'] = pd.to_numeric(elec_df[total_col], errors='coerce') / pd.to_numeric(elec_df[num_col], errors='coerce')
                else: 
                    continue
            
            #Merge and Map
            merged_df = pd.merge(elec_df, sspl_df, on="Postcode", how="left")
            merged_df['Council_Area'] = merged_df['Council_Code'].map(mapping_dict)
            
            #Aggregate
            grouped = merged_df.groupby('Council_Area')['Target_Value'].mean().reset_index()
            grouped['Year'] = year
            yearly_aggregates.append(grouped)
            
        except Exception:
            continue

    print("Done.")

    #Final Calculation and Output
    if not yearly_aggregates:
        print("No valid data processed.")
        sys.exit(1)

    final_df = pd.concat(yearly_aggregates, ignore_index=True)
    pivot_df = final_df.pivot(index='Council_Area', columns='Year', values='Target_Value')
    
    if 2015 in pivot_df.columns and 2023 in pivot_df.columns:
        pivot_df['Change_kWh'] = pivot_df[2023] - pivot_df[2015]
        pivot_df['Change_Pct'] = (pivot_df['Change_kWh'] / pivot_df[2015]) * 100
        
        # Sort by Percentage Change
        result_df = pivot_df.sort_values(by='Change_Pct', ascending=True)
        
        print("\n" + "="*85)
        print(f"{'Council Area':<30} | {'2015 (kWh)':<12} | {'2023 (kWh)':<12} | {'Change (%)':<10}")
        print("-" * 85)
        
        for council, row in result_df.iterrows():
            print(f"{council:<30} | {row[2015]:.1f}        | {row[2023]:.1f}        | {row['Change_Pct']:>+7.2f}%")
        
        print("=" * 85)
        
        cols_to_save = [c for c in pivot_df.columns if isinstance(c, int) or c in ['Change_kWh', 'Change_Pct']]
        result_df[cols_to_save].to_csv(OUTPUT_FILE)
        print(f"Ranked results saved to: {OUTPUT_FILE}")
        
    else:
        print("Insufficient data to calculate 2015-2023 changes.")

if __name__ == "__main__":
    main()