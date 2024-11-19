import streamlit as st
import plotly.express as px
import pandas as pd  # Missing import for pandas

# Load the data
data = pd.read_csv("C:/Users/pc click/immo_eliza_analysis/immoweb_data_cleaned.csv")

# Ensure data columns are correctly typed
print(data[["Living_Area", "Price", "Number_of_Rooms"]].dtypes)

# Remove rows with missing values in relevant columns
filtered_data = data.dropna(subset=["Living_Area", "Price", "Number_of_Rooms"])

# Dashboard Title
st.title("Real Estate Interactive Dashboard")

# Sidebar Filters
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

# Filtered Data based on sidebar selections
filtered_data = filtered_data[
    (filtered_data["Type_of_Property"].isin(property_type)) &
    (filtered_data["State_of_the_Building"].isin(state_of_building))
]

# Main Dashboard: Display filtered data
st.header("Filtered Properties")
st.dataframe(filtered_data)

# Plot Price vs Living Area
st.header("Price vs Living Area")
fig = px.scatter(
    filtered_data,
    x="Living_Area",
    y="Price",
    color="Type_of_Property",
    size="Number_of_Rooms",
    hover_data=["Subtype_of_Property"],
    template="plotly"  # Use the default template
)
st.plotly_chart(fig)

# Distribution of Prices
st.header("Price Distribution")
fig2 = px.histogram(filtered_data, x="Price", nbins=20, color="Type_of_Property", template="plotly")
st.plotly_chart(fig2)
