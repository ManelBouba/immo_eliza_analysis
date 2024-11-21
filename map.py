import pandas as pd
import plotly.express as px
import geopandas as gpd

# Load cleaned real estate data
data = pd.read_csv("C:/Users/pc click/immo_eliza_analysis/immoweb_data_cleaned.csv")

# Aggregate price by commune (replace 'Locality' with the correct column name in your dataset)
commune_prices = data.groupby("Locality").agg({"Price": "mean"}).reset_index()
commune_prices.columns = ["Commune", "Average_Price"]

# Load Belgium Commune GeoJSON
commune_geojson = gpd.read_file("belgium_communes.geojson")  # GeoJSON file with communes

# Merge price data with GeoJSON based on commune name
merged_data = commune_geojson.merge(commune_prices, left_on="name", right_on="Commune", how="left")

# Create a choropleth map
fig = px.choropleth_mapbox(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,  # Use GeoDataFrame index for mapping
    color="Average_Price",
    hover_name="Commune",
    hover_data=["Average_Price"],
    color_continuous_scale="Viridis",
    labels={"Average_Price": "Price (€)"},
    title="Average Property Prices by Commune in Belgium",
    mapbox_style="carto-positron",
    center={"lat": 50.5039, "lon": 4.4699},  # Center of Belgium
    zoom=7,
)

# Adjust the map's appearance
fig.update_geos(fitbounds="locations", visible=False)  # Fit the map to the locations

# Show the map
fig.show()
