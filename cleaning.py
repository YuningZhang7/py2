import pandas as pd
import numpy as np
data = pd.read_csv('https://assets.publishing.service.gov.uk/media/6762f20f3229e84d9bbde81f/Postcode_level_all_meters_electricity_2021.csv')
#We want to remove the postcodes which are not in scotland
# List of Scottish postcodes
scot_postcodes = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV', 'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']
# Copy list so we don't delete the original
clean_data = data.copy()
# Ensures that all Outcodes as type string with no spaces around the edges and are uppercase
clean_data['Outcode'] = clean_data['Outcode'].astype(str).str.strip().str.upper()
# Keep only the rows with Scottish postcodes
clean_data = clean_data[clean_data['Outcode'].str.startswith(tuple(scot_postcodes))]
clean_data = clean_data[~clean_data['Outcode'].str.startswith(('GU', 'GL'))]
# Print the starts of outcodes and how many postcodes are within each one
print(clean_data['Outcode'].str.extract(r'^([A-Z]{1,2})')[0].value_counts())
# Print the length of the clean data
print(f"Remaining rows: {len(clean_data)}")
# Export data to csv
clean_data.to_csv('electricity_scotland_clean_2021.csv', index=False)

info_2015 = pd.read_csv('https://assets.publishing.service.gov.uk/media/6762e8dbe6ff7c8a1fde9b2c/Postcode_level_all_meters_electricity_2015.csv')
clean_2015 = info_2015.copy()

#Got from chatgpt - create new column with city codes 

clean_2015['City'] = clean_2015['Outcode'].str.strip('0123456789')
clean_2015 = clean_2015[clean_2015['City'].isin(scot_postcodes)]

clean_2015.to_csv('electricity_scotland_clean_2015.csv',index=False)

#Cleaning data 
info_2016 = pd.read_csv('https://assets.publishing.service.gov.uk/media/6762e9b2e6ff7c8a1fde9b30/Postcode_level_all_meters_electricity_2016.csv')
clean_2016 = info_2016.copy()

clean_2016['City'] = clean_2016['Outcode'].str.strip('0123456789')

clean_2016 = clean_2016[clean_2016['City'].isin(scot_postcodes)]

clean_2016.to_csv('electricity_scotland_clean_2016.csv',index=False)
