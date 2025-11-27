import pandas as pd
import numpy as np
electricity_data = pd.read_csv('cleaning data with code/clean_data/electricity_scotland_2023.csv')
postcode_data = pd.read_csv('council area with elec consumption/Scottish_Postcode_Lookup_2025_1.csv')

#Need only postcode data and data zone 2011code
postcode_data = postcode_data[['Postcode','DataZone2011Code']]


house_data = pd.read_csv('housing_data.csv')

columns_needed = ['Data Zone','Whole house or bungalow: Total','Flat, maisonette or apartment: Total','Caravan or other mobile or temporary structure']
house_data = house_data[columns_needed]
#print(house_data.head())

#Adding postcode to house data

#Find postcode for a given datazone

#house_data = house_data.merge(postcode_data[['DataZone2011Code', 'Postcode']],left_on='Data Zone',right_on='DataZone2011Code',  how='left')

electricity_data = electricity_data.merge(postcode_data[['DataZone2011Code', 'Postcode']],left_on='Postcode',right_on='Postcode',how='left')
#location = postcode_data[house_data['Data Zone']==postcode_data['DataZone2011Code']].loc[:,'Postcode']
#house_data['Postcode'] = postcode_data[house_data['Data Zone']==postcode_data['DataZone2011Code']]['Postcode']
#print(house_data.columns)

electricity_data= electricity_data.drop(['Num_meters','Mean_cons_kwh','Median_cons_kwh'],axis=1)
electricity_data['Consumption for datazone'] = electricity_data.groupby('DataZone2011Code')['Total_cons_kwh'].transform('sum')


data_zone_electricity = electricity_data.drop_duplicates('DataZone2011Code')
data_zone_electricity = data_zone_electricity.drop(['Outcode','Postcode','Total_cons_kwh'],axis=1)


house_data_electricity = house_data.merge(data_zone_electricity[['DataZone2011Code', 'Consumption for datazone']],left_on='Data Zone',right_on='DataZone2011Code',  how='left')

house_data_electricity['Whole house or bungalow: Total'] = (
    house_data_electricity['Whole house or bungalow: Total']
    .str.rstrip('%')          # remove % at the end
    .astype(float)            # convert to float
)

house_data_electricity['Flat, maisonette or apartment: Total'] = (
    house_data_electricity['Flat, maisonette or apartment: Total']
    .str.rstrip('%')          # remove % at the end
    .astype(float)            # convert to float
)

house_data_electricity['Caravan or other mobile or temporary structure'] = (
    house_data_electricity['Caravan or other mobile or temporary structure']
    .str.rstrip('%')          # remove % at the end
    .astype(float)            # convert to float
)

house_data_electricity['Whole House'] = (house_data_electricity['Whole house or bungalow: Total'] >= 90).astype(int)
house_data_electricity['Flats'] = (house_data_electricity['Flat, maisonette or apartment: Total'] >= 90).astype(int)
house_data_electricity['Other'] = (house_data_electricity['Caravan or other mobile or temporary structure'] >= 90).astype(int)


flat_electricity = house_data_electricity[house_data_electricity['Flats']==1]
whole_house_electricity = house_data_electricity[house_data_electricity['Whole House']==1]

print(flat_electricity.describe())
print(whole_house_electricity.describe())

#Boxplot this info



