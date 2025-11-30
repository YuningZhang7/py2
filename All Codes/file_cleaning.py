"""
This code file gets data stored for analysis from the urls

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

    for year in range(2015, 2024):
        url = DATA_URLS.get(year)
        get_scottish_data(year, url)

    print("All files downloaded for analysis.")    


