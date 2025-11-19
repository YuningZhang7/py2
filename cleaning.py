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


#The Year-on_Year(YOY) is used in this project to measure how Scotland’s electricity consumption changes from one year to the next.
#YoY focuses on short-term dynamics by comparing each year’s total electricity demand with that of the previous year.

#YoY analysis allows us to identify whether consumption was potentially affected by some external facts, such as:
#warmer winters, behavioural changes, and disruption such as COVID-19 pandemic.


import pandas as pd

# Import the datasets.

# Create a new column named "Year" so we always know which year each row belongs to.
df_2015 = pd.read_csv("electricity_scotland_clean_2015.csv")
df_2015["Year"] = 2015 # Add a 'Year' column so we always know which year each row belongs to.
# Removes any row where the Postcode column contains the text "All postcodes".
df_2015 = df_2015[
    ~df_2015["Postcode"].str.contains("All postcodes", case=False, na=False)
]


df_2016 = pd.read_csv("electricity_scotland_clean_2016.csv")
df_2016["Year"] = 2016
df_2016 = df_2016[
    ~df_2016["Postcode"].str.contains("All postcodes", case=False, na=False)
]

# Combine all years into one dataframe.
data = pd.concat(
    [df_2015, df_2016,],   # add extra dfs here if you create them.
    ignore_index=True
)


# Calculate total Scotland consumption per year.
yearly = (
    data.groupby("Year")["Total_cons_kwh"]   # group by Year, focus on Total_cons_kwh
        .sum()                               # sum consumption within each year
        .reset_index()                       # turn the result back into a normal df
        .sort_values("Year")                 
)

# Rename column to a clearer name for the final table
yearly = yearly.rename(columns={"Total_cons_kwh": "Total_scotland_cons_kwh"})

# Finaily calculate the YOY change.
# Difference in total consumption compared to previous year.
# Example: YoY_change_kwh(2016) = Total_2016 - Total_2015.

# Absolute change in kWh.
# For each row, subtract the previous row’s value.
yearly["YoY_change_kwh"] = yearly["Total_scotland_cons_kwh"].diff() # Used diff function so we could automatically computes differences row-by-row. 

# Percentage change (%)\
# pct_change funvction used to calculates percentage change between the current row and the previous row.
yearly["YoY_change_pct"] = yearly["Total_scotland_cons_kwh"].pct_change() * 100

# Round percentage for neat printing
yearly["YoY_change_pct"] = yearly["YoY_change_pct"].round(2)



import pandas as pd

#This analysis measures how stable Scotland’s electricity consumption.
#It calculates the mean, variance, standard deviation, and coefficient of variation to show how much consumption changes from year to year.

yearly = pd.read_csv("yoy_scotland_results.csv")

cons = yearly["Total_scotland_cons_kwh"] # Pick only the consumption column

mean_consumption = cons.mean()
variance_consumption = cons.var()
std_consumption = cons.std()

# Coefficient of variation (CV) = Std / Mean * 100 (%)
cv_consumption = (std_consumption / mean_consumption) * 100 #This gives a percentage showing how variable the data is relative to the average.

print("\n=== Summary statistics for annual consumption ===")
print(f"Mean consumption       : {mean_consumption:,.2f} kWh")
print(f"Variance               : {variance_consumption:,.2f} (kWh^2)")
print(f"Standard deviation     : {std_consumption:,.2f} kWh")
print(f"Coefficient of variation: {cv_consumption:.2f} %")
