import pandas as pd

house_data = pd.read_csv('DataZoneHouseholdData.csv')
clean_house_data = house_data.copy()
columns_to_remove = ['All occupied households', 'Whole house or bungalow: Detached', 'Whole house or bungalow: Semi-detached', 'Whole house or bungalow: Terraced (including end-terrace)', 'Flat, maisonette or apartment: Purpose-built block of flats or tenement', 'Flat, maisonette or apartment: Part of a converted or shared house (including bed-sits)', 'Flat, maisonette or apartment: In a commercial building']

for col in columns_to_remove[col]:
    clean_house_data.drop(col, inplace=True, axis=1)