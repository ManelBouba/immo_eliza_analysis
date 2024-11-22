import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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

# Display filtered data
st.header("Filtered Data")
st.write(f"Number of records after applying filters: {len(filtered_data)}")
st.dataframe(filtered_data)

# # Correlation Heatmap
# st.header("Correlation Heatmap")
# # Calculate correlation matrix
# correlation_matrix = filtered_data.corr()

# # # Create a seaborn heatmap for correlation matrix
# # fig3, ax = plt.subplots(figsize=(10, 8))
# # sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, cbar_kws={'shrink': 0.8})
# # st.pyplot(fig3)

# # # Correlation Plotly Interactive
# # st.header("Interactive Correlation Plot")
# # Create a Plotly Heatmap
# fig4 = go.Figure(data=go.Heatmap(
#     z=correlation_matrix.values,
#     x=correlation_matrix.columns,
#     y=correlation_matrix.columns,
#     colorscale="YlGnBu",
#     colorbar=dict(title="Correlation Coefficient")
# ))
# fig4.update_layout(
#     title="Correlation Heatmap (Interactive)",
#     xaxis_title="Variables",
#     yaxis_title="Variables"
# )
# st.plotly_chart(fig4)

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
df=pd.read_csv("C:/Users/pc click/immo_eliza_analysis/immoweb_data_cleaned.csv")
# Price per Locality
st.header("Average Price per Locality")
avg_price_locality = df.groupby("Municipality")["Price"].mean().reset_index().sort_values(by="Price", ascending=False)
locality_price_fig = px.bar(
    avg_price_locality.head(20),
    x="Municipality",
    y="Price",
    title="Top 20 Localities by Average Price",
    template="plotly_dark"
)
st.plotly_chart(locality_price_fig)

# Boxplot of Price by Property Type
st.header("Price Distribution by Property Type")
boxplot_fig = px.box(
    filtered_data,
    x="Type_of_Property",
    y="Price",
    color="Type_of_Property",
    title="Boxplot of Price by Property Type",
    template="plotly_dark"
)
st.plotly_chart(boxplot_fig)

# Pairwise Correlations
st.header("Pairwise Relationships")
pairwise_fig = px.scatter_matrix(
    filtered_data,
    dimensions=["Living_Area", "Price", "Number_of_Rooms"],
    color="Type_of_Property",
    title="Pairwise Correlation of Key Variables",
    template="plotly_dark"
)
st.plotly_chart(pairwise_fig)

# Save transformed data if needed
filtered_data.to_csv("C:/Users/pc click/immo_eliza_analysis/immoweb_data_filtered.csv", index=False)
st.write("Filtered data saved to 'immoweb_data_filtered.csv'.")
