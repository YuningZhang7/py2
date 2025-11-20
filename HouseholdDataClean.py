import pandas as pd

house_data = pd.read_csv('housing_data.csv')
clean_house_data = house_data.copy()
columns_to_remove = ['All occupied households', 'Whole house or bungalow: Detached', 'Whole house or bungalow: Semi-detached', 'Whole house or bungalow: Terraced (including end-terrace)', 'Flat, maisonette or apartment: Purpose-built block of flats or tenement', 'Flat, maisonette or apartment: Part of a converted or shared house (including bed-sits)', 'Flat, maisonette or apartment: In a commercial building']


clean_house_data = clean_house_data.drop(columns_to_remove,axis=1)

print(clean_house_data.columns)
