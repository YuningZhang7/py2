import pandas as pd

# Read the dataset from the "data" folder
data = pd.read_csv("data/Postcode_level_all_meters_electricity_2020.csv")


# Define postcode areas in Scotland
scotland_areas = ['AB', 'DD', 'DG', 'EH', 'FK', 'G', 'HS', 'IV',
                  'KA', 'KW', 'KY', 'ML', 'PA', 'PH', 'TD', 'ZE']

# Make sure postcode column is clean (no spaces, all uppercase)
data['Postcode'] = data['Postcode'].astype(str).str.strip().str.upper()

# Extract only the letter part (postcode area, e.g. "EH" from "EH8 9AG")
data['Area'] = data['Postcode'].str.extract(r'^([A-Z]{1,2})')

# Keep rows where the area is in the Scotland list
scotland_data = data[data['Area'].isin(scotland_areas)]

# Save the filtered data to a new file
scotland_data.to_csv("electricity_scotland_2020.csv", index=False)

print("Scotland data saved successfully!")
print("Rows kept:", len(scotland_data))
