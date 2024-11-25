import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

#Load the shapefile
belgium_provinces = gpd.read_file("gadm41_BEL_shp/gadm41_BEL_2.shp")
df= pd.read_csv("immoweb_data_cleaned.csv")
#Correct province names in df_prices to match those in 'NAME_2'
avg_prices = df.groupby('Province')['Price'].mean()
print(avg_prices)
province_prices = {
    'Province': ['Antwerpen', 'Oost-Vlaanderen', 'Vlaams Brabant', 'Limburg', 'Bruxelles',
                 'West-Vlaanderen', 'Hainaut', 'Liège', 'Luxembourg', 'Namur', 'Brabant Wallon'],
    'Average_Price': [438205.377339, 540219.800177, 425228.522432, 503296.125463, 280955.284305,
                      389069.238953, 287215.295034, 344578.879552, 290432.886943, 518969.222973, 623104.564666]
}
df_prices = pd.DataFrame(province_prices)

#Merge the data
belgium_provinces = belgium_provinces.merge(df_prices, left_on='NAME_2', right_on='Province', how='left')

#Verify the merge
print(belgium_provinces[['NAME_2', 'Average_Price']])
print("Number of missing Average_Price values:", belgium_provinces['Average_Price'].isna().sum())

#Ensure 'Average_Price' is numeric
belgium_provinces['Average_Price'] = pd.to_numeric(belgium_provinces['Average_Price'], errors='coerce')

#Re-project to a suitable CRS
belgium_provinces = belgium_provinces.to_crs(epsg=31370)  # Belgian Lambert 72 CRS

#Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
belgium_provinces.plot(
    column='Average_Price',
    ax=ax,
    legend=True,
    cmap='OrRd',
    edgecolor='black',
    missing_kwds={
        "color": "lightgrey",
        "edgecolor": "red",
        "hatch": "///",
        "label": "Missing values",
    }
)

ax.set_title('Average Property Prices by Province in Belgium', fontsize=15)
ax.axis('off')

#Adjust legend position only if legend exists
leg = ax.get_legend()
if leg is not None:
    leg.set_bbox_to_anchor((1.15, 0.5))
else:
    print("Legend was not created.")
plt.show()