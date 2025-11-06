import pandas as pd
data = pd.read_csv('https://assets.publishing.service.gov.uk/media/6762f39cff2c870561bde826/Postcode_level_all_meters_electricity_2023.csv')
print(data.head())
#We want to remove the postcodes which are not in scotland
