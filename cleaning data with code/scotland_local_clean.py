"""
Data Cleaning & Extraction Script.

This script handles the ETL (Extract, Transform, Load) process:
1.  Connects to UK Government servers to stream electricity data CSVs.
2.  Filters the data on-the-fly to retain only Scottish postcodes.
3.  Saves the processed, smaller datasets locally for analysis.

"""

import pandas as pd
from pathlib import Path
import re
import os

OUTPUT_DIR = "clean_data"

# Set of Postcode Area prefixes belonging to Scotland
SCOT_AREAS = ["AB", "DD", "DG", "EH", "FK", "G", "HS", "IV", 
              "KA", "KW", "KY", "ML", "PA", "PH", "TD", "ZE"]



# Direct download URLs for UK electricity consumption data (2015-2023)
DATA_URLS = {
    2023: "https://assets.publishing.service.gov.uk/media/6762f39cff2c870561bde826/Postcode_level_all_meters_electricity_2023.csv",
    2022: "https://assets.publishing.service.gov.uk/media/6762f29ecdb5e64b69e307db/Postcode_level_all_meters_electricity_2022.csv", 
    2021: "https://assets.publishing.service.gov.uk/media/6762f20f3229e84d9bbde81f/Postcode_level_all_meters_electricity_2021.csv",
    2020: "https://assets.publishing.service.gov.uk/media/6762f10dff2c870561bde823/Postcode_level_all_meters_electricity_2020.csv",
    2019: "https://assets.publishing.service.gov.uk/media/6762ec0c4e2d5e9c0bde9b2a/Postcode_level_all_meters_electricity_2019.csv",
    2018: "https://assets.publishing.service.gov.uk/media/6762eb504e2d5e9c0bde9b26/Postcode_level_all_meters_electricity_2018.csv",
    2017: "https://assets.publishing.service.gov.uk/media/6762ea7bbe7b2c675de307c9/Postcode_level_all_meters_electricity_2017.csv",
    2016: "https://assets.publishing.service.gov.uk/media/6762e9b2e6ff7c8a1fde9b30/Postcode_level_all_meters_electricity_2016.csv",
    2015: "https://assets.publishing.service.gov.uk/media/6762e8dbe6ff7c8a1fde9b2c/Postcode_level_all_meters_electricity_2015.csv"
}

#HELPER FUNCTIONS
#Do we really need the following function?

def find_postcode_col(columns: list) -> str | None:
    """
    Identifies the column name containing postcodes from a list of columns.
    Handles variations in naming conventions

    Args:
    columns (list): A list of column names from the dataframe.

    Returns:
    str | None: The detected column name, or None if not found.
    """
    #Check for exact match
    for col in columns:
        if col.strip().lower() == "postcode":
            return col
    
    #Check for partial match containing both keywords
    for col in columns:
        lower_col = col.lower()
        if "post" in lower_col and "code" in lower_col:
            return col
            
    return None


def filter_scotland_chunk(df: pd.DataFrame, postcode_col: str) -> pd.DataFrame:
    """
    Filters a dataframe chunk to retain only rows corresponding to Scottish postcodes.

    Args:
    df (pd.DataFrame): The dataframe chunk to filter.
    postcode_col (str): The name of the column containing postcode data.

    Returns:
    pd.DataFrame: A copy of the dataframe containing only Scottish records.
    """
    # Ensure postcodes are strings, remove whitespace, and convert to uppercase
    postcode_series = df[postcode_col].astype(str).str.strip().str.upper()
    
    #clean_2016['City'] = clean_2016['Outcode'].str.strip('0123456789')

    #clean_2016 = clean_2016[clean_2016['City'].isin(scot_postcodes)]
    # Extract the Area Prefix
    area_prefix = postcode_series.str.extract(AREA_RE, expand=False)
    
    # Filter rows where the prefix exists in the predefined Scottish set
    return df.loc[area_prefix.isin(SCOT_AREAS)].copy()

def filter_scotland_chunk(dataset):
    """
    Filters a dataframe to retain only rows corresponding to Scottish postcodes.

    Input: Dataset of all electricity data across UK with outcode information

    Returns: A copy of the dataframe containing only Scottish records.
    """

    clean_dataset = dataset.copy()
    clean_dataset['City Code'] = clean_dataset['Outcode'].str.strip('0123456789')
    clean_dataset= clean_dataset[clean_dataset['City Code'].isin(SCOT_AREAS)]
    clean_dataset = clean_dataset.drop(['City Code'],axis =1)
    return clean_dataset

def get_scottish_data(year, url):

    # Folder where files will be saved
    folder = "clean_data"

    #If folder does not exist, then create
    os.makedirs(folder, exist_ok=True)

    # Full path to the output CSV
    filename = f"{folder}/electricity_scotland_{year}.csv"


    # If file already exists, load and return it
    if os.path.exists(filename):
        print(f"[{year}] We already have the file!")
        data = pd.read_csv(filename, dtype=str)
        return data
    else: 
        df = pd.read_csv(url, dtype=str, low_memory=False)
        scot_data = filter_scotland_chunk(df)
        scot_data.to_csv(filename, index=False)
        return pd.read_csv(filename, dtype=str)


if __name__ == "__main__":
    print("Scotland Electricity Data Cleaner")
    print(f"Output Directory: {OUTPUT_DIR}")

    for year in range(2015, 2024):
        url = DATA_URLS.get(year)
        get_scottish_data(year, url)

    print("All files downloaded for analysis.")    


def process_url_to_clean_csv(year: int, url: str, output_path: Path) -> bool:
    """
    Streams data from a URL, filters for Scotland, and saves to a local CSV.
    
    Uses a chunk-based approach to handle large files without loading the entire dataset into memory.

    Args:
    year (int): The year of the dataset (for logging purposes).
    url (str): The direct download URL of the CSV file.
    output_path (Path): The local path where the cleaned file should be saved.

    Returns:
    bool: True if successful, False otherwise.
    """
    print(f"[{year}] Starting download and processing stream")
    
    try:
        # Create the output directory if it does not exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        chunk_size = 100000  # Number of rows to process at a time
        first_chunk = True
        total_rows = 0
        
        # Read CSV in chunks directly from the URL
        with pd.read_csv(url, chunksize=chunk_size, dtype=str, low_memory=False) as reader:
            for chunk in reader:
                #Identify the postcode column dynamically
                postcode_col = find_postcode_col(chunk.columns)
                
                if not postcode_col:
                    print(f"[{year}] Error: Could not find Postcode column.")
                    return False
                
                #Filter the current chunk for Scottish data
                scot_data = filter_scotland_chunk(chunk, postcode_col)
                
                if not scot_data.empty:
                    #Append to the local file
                    # Write header only for the first chunk
                    mode = 'w' if first_chunk else 'a'
                    include_header = first_chunk
                    
                    scot_data.to_csv(output_path, index=False, mode=mode, header=include_header)
                    
                    total_rows += len(scot_data)
                    first_chunk = False
                    
        print(f"[{year}] Success Saved {total_rows} rows to: {output_path.name}")
        return True

    except Exception as e:
        print(f"[{year}] Failed during processing: {e}")
        return False


#MAIN EXECUTION

if __name__ == "__main__":
    print("Scotland Electricity Data Cleaner")
    print(f"Output Directory: {OUTPUT_DIR}\n")
    
    # Ensure the output directory exists before starting
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()

    for year in range(2015, 2024):
        output_file = OUTPUT_DIR / f"electricity_scotland_{year}.csv"
        url = DATA_URLS.get(year)
        
        # Skip processing if the file already exists locally (Caching)
        if output_file.exists():
            print(f"[{year}] Skipped: File already exists.")
            continue
            
        # Verify a valid URL exists for the year
        if not url or "http" not in url:
            print(f"[{year}] Skipped: No valid URL configuration.")
            continue
            
        # Run the streaming and filtering process
        process_url_to_clean_csv(year, url, output_file)

    print("\nAll tasks completed. Data is ready for analysis.")