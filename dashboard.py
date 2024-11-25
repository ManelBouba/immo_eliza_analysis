import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
# Load the data
data = pd.read_csv("C:/Users/pc click/immo_eliza_analysis/immoweb_data_cleaned.csv")

# Ensure data columns are correctly typed
st.sidebar.title("Data Overview and Filters")

# Display dataset overview
if st.sidebar.checkbox("Show Raw Data", value=False):
    st.subheader("Dataset Overview")
    st.write(data)

# Drop rows with missing values in key columns for analysis
filtered_data = data.dropna(subset=["Living_Area", "Price", "Number_of_Rooms"])

# Sidebar Filters
st.sidebar.subheader("Filter Options")
property_type = st.sidebar.multiselect(
    "Select Property Type:",
    options=data["Type_of_Property"].unique(),
    default=data["Type_of_Property"].unique()
)

state_of_building = st.sidebar.multiselect(
    "Select State of the Building:",
    options=data["State_of_the_Building"].unique(),
    default=data["State_of_the_Building"].unique()
)

# Apply filters
filtered_data = filtered_data[
    (filtered_data["Type_of_Property"].isin(property_type)) &
    (filtered_data["State_of_the_Building"].isin(state_of_building))
]

# Dashboard Title
st.title("Real Estate Interactive Dashboard")

# # Display filtered data
# st.header("Filtered Data")
# st.write(f"Number of records after applying filters: {len(filtered_data)}")
# st.dataframe(filtered_data)

# Key statistics (mean, median, etc.) for numerical columns
st.subheader("Key Statistics")
st.write(filtered_data.describe())

# Price vs Living Area Scatter Plot
st.header("Price vs Living Area")
scatter_fig = px.scatter(
    filtered_data,
    x="Living_Area",
    y="Price",
    color="Type_of_Property",
    size="Number_of_Rooms",
    hover_data=["Subtype_of_Property"],
    template="plotly_dark"
)
st.plotly_chart(scatter_fig)

# Distribution of Prices
st.header("Price Distribution")
price_dist_fig = px.histogram(
    filtered_data,
    x="Price",
    nbins=30,
    color="Type_of_Property",
    title="Price Distribution by Property Type",
    template="plotly_dark"
)
st.plotly_chart(price_dist_fig)

# Living Area Distribution
st.header("Living Area Distribution")
living_area_fig = px.histogram(
    filtered_data,
    x="Living_Area",
    nbins=30,
    color="Type_of_Property",
    title="Living Area Distribution by Property Type",
    template="plotly_dark"
)
st.plotly_chart(living_area_fig)

# Average Price per Locality
st.header("Average Price per Locality")
avg_price_locality = data.groupby("Municipality")["Price"].mean().reset_index().sort_values(by="Price", ascending=False)
locality_price_fig = px.bar(
    avg_price_locality.head(20),
    x="Municipality",
    y="Price",
    title="Top 20 Localities by Average Price",
    template="plotly_dark"
)
st.plotly_chart(locality_price_fig)


# Filtered data based on selected features' impact
state_of_building_data = filtered_data[['State_of_the_Building', 'Price']].groupby('State_of_the_Building').mean().reset_index()
number_of_rooms_data = filtered_data[['Number_of_Rooms', 'Price']].groupby('Number_of_Rooms').mean().reset_index()
fully_equipped_kitchen_data = filtered_data[['Fully_Equipped_Kitchen', 'Price']].groupby('Fully_Equipped_Kitchen').mean().reset_index()
terrace_data = filtered_data[['Terrace', 'Price']].groupby('Terrace').mean().reset_index()

# State of the Building Impact
st.write("### Impact of State of the Building on Price")
st.write("How does the condition of the building affect its price?")
st.write(state_of_building_data)

# Number of Rooms Impact
st.write("### Impact of Number of Rooms on Price")
st.write("How does the number of rooms affect the price?")
st.write(number_of_rooms_data)

# Fully Equipped Kitchen Impact
st.write("### Impact of Fully Equipped Kitchen on Price")
st.write("How does having a fully equipped kitchen influence the price?")
st.write(fully_equipped_kitchen_data)


# Terrace Impact
st.write("### Impact of Terrace on Price")
st.write("Does having a terrace affect the price?")
st.write(terrace_data)

# Save transformed data if needed
filtered_data.to_csv("C:/Users/pc click/immo_eliza_analysis/immoweb_data_filtered.csv", index=False)
st.write("Filtered data saved to 'immoweb_data_filtered.csv'.")


# Real Estate Prices Data (You can also load this from a CSV or a database if required)
real_estate_prices = {
    'Region': ['Belgium', 'Belgium', 'Wallonia', 'Wallonia', 'Flanders', 'Flanders', 'Brussels', 'Brussels'],
    'Municipality': ['Knokke-Heist', 'Vaux-sur-Sûre', 'Lasne', 'Vaux-sur-Sûre', 'Knokke-Heist', 'Alveringem', 'Ixelles', 'Molenbeek-Saint-Jean'],
    'Type': ['Most Expensive', 'Least Expensive', 'Most Expensive', 'Least Expensive', 'Most Expensive', 'Least Expensive', 'Most Expensive', 'Least Expensive'],
    'Average Price (EUR)': [601451.55, 125000.00, 395000.00, 125000.00, 601451.55, 169000.00, 458077.52, 264723.60],
    'Median Price (EUR)': [599000.00, 125000.00, 395000.00, 125000.00, 599000.00, 169000.00, 415000.00, 239000.00],
    'Price per Square Meter (EUR)': [7464.10, 657.89, 4030.61, 657.89, 7464.10, 840.79, 4563.30, 2796.30]
}

# Convert to DataFrame
real_estate_df = pd.DataFrame(real_estate_prices)

# Display the Real Estate Prices Table
st.header("Real Estate Prices in Belgium")
st.write("This table displays average, median prices, and price per square meter for various regions and municipalities in Belgium.")

# Display the table
st.table(real_estate_df)


# Load the shapefile for Belgian provinces
belgium_provinces = gpd.read_file("gadm41_BEL_shp/gadm41_BEL_2.shp")

# Load the property data
df = pd.read_csv("immoweb_data_cleaned.csv")

# Correct province names in df_prices to match those in 'NAME_2'
province_prices = {
    'Province': ['Antwerpen', 'Oost-Vlaanderen', 'Vlaams Brabant', 'Limburg', 'Bruxelles',
                 'West-Vlaanderen', 'Hainaut', 'Liège', 'Luxembourg', 'Namur', 'Brabant Wallon'],
    'Average_Price': [438205.377339, 540219.800177, 425228.522432, 503296.125463, 280955.284305,
                      389069.238953, 287215.295034, 344578.879552, 290432.886943, 518969.222973, 623104.564666]
}

df_prices = pd.DataFrame(province_prices)

# Merge the data
belgium_provinces = belgium_provinces.merge(df_prices, left_on='NAME_2', right_on='Province', how='left')

# Ensure 'Average_Price' is numeric
belgium_provinces['Average_Price'] = pd.to_numeric(belgium_provinces['Average_Price'], errors='coerce')

# Re-project to a suitable CRS (Belgium Lambert 72 CRS)
belgium_provinces = belgium_provinces.to_crs(epsg=4326)  # WGS84 CRS for compatibility with Plotly

# Convert GeoDataFrame to DataFrame for Plotly
belgium_provinces_df = belgium_provinces[['NAME_2', 'Average_Price', 'geometry']]

# Create a Plotly map
fig = px.choropleth(
    belgium_provinces_df,
    geojson=belgium_provinces_df.geometry,
    locations=belgium_provinces_df.index,
    color='Average_Price',
    hover_name='NAME_2',
    color_continuous_scale="OrRd",
    labels={'Average_Price': 'Average Price (EUR)', 'NAME_2': 'Province'},
    title="Average Property Prices by Province in Belgium"
)

# Update layout for better visualization
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    geo=dict(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white"),
    coloraxis_colorbar_title="Price (EUR)"
)

# Show the Plotly map in Streamlit
st.title("Real Estate Prices in Belgium by Province")
st.plotly_chart(fig)
