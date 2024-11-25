import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import numpy as np
import matplotlib.patches as mpatches

# Load your dataset
data = pd.read_csv("immoweb_data_cleaned.csv")

# Step 2: Remove 'Province' and 'Locality' columns
data = data.drop(columns=['Province', 'Locality'], errors='ignore')  # 'errors' ensures no error if columns don't exist

# Step 3: Apply State Mapping
state_mapping = {
    'TO_BE_DONE_UP': 0,
    'TO_RENOVATE': 1,
    'JUST_RENOVATED': 2,
    'GOOD': 3,
    'AS_NEW': 4
}

if 'State_of_the_Building' in data.columns:
    data['State_of_the_Building'] = data['State_of_the_Building'].map(state_mapping)

# Aggregating 'Locality' for meaningful analysis
if 'Municipality' in data.columns:  
    locality_agg = data.groupby('Municipality')['Price'].mean().reset_index().rename(columns={'Price': 'Average_Price'})
    # st.write("Top Localities by Average Price:")
    # st.write(locality_agg.sort_values(by='Average_Price', ascending=False).head())

# Step 4: Separate numeric and categorical columns
numeric_cols = data.select_dtypes(include=['number']).columns
categorical_cols = data.select_dtypes(include=['object']).columns

# st.write(f"Numeric columns: {numeric_cols}")
# st.write(f"Categorical columns: {categorical_cols}")

# Step 5: Encode categorical columns for correlation analysis
label_encoder = LabelEncoder()
encoded_data = data.copy()
for col in categorical_cols:
    encoded_data[col] = label_encoder.fit_transform(data[col].astype(str))

# Save the full correlation matrix to a CSV file
encoded_data.to_csv("encoded_data.csv", index=True)

# Step 6: Compute correlation matrix
correlation_matrix = encoded_data.corr()

# Step 7: Display correlation with target variable 'Price'
if 'Price' in correlation_matrix.columns:  
    st.subheader("Correlation of Variables with Price")
    
    # Calculate correlation with Price
    correlation_with_price = correlation_matrix["Price"].sort_values(ascending=False)
    
    # Display correlation values in the dashboard
    # st.write("### Correlation Values with 'Price':")
    # st.dataframe(correlation_with_price.to_frame())
    
    # Visualization: Correlation Heatmap with Price
    plt.figure(figsize=(10, 6))
    sns.heatmap(
        correlation_with_price.to_frame(),
        annot=True, cmap="coolwarm", fmt=".2f", cbar_kws={"shrink": 0.8}
    )
    plt.title("Correlation of Variables with Price")
    plt.tight_layout()
    
    # Display the heatmap in the dashboard
    st.pyplot(plt)

# Create heatmap
st.subheader("Correlation Heatmap with Highlighted Relationships")
plt.figure(figsize=(14, 10))
sns.heatmap(
    correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar_kws={"shrink": 0.8}
)

highlighted_correlations = [
    ('Type_of_Property', 'Subtype_of_Property', 'strong_pos'),  # Strong positive
    ('Living_Area', 'Number_of_Rooms', 'strong_pos'),
    ('Surface_area_plot_of_land', 'Type_of_Property', 'strong_pos'),
    ('Surface_area_plot_of_land', 'Subtype_of_Property', 'moderate_pos'),  # Moderate positive
    ('Number_of_Rooms', 'Type_of_Property', 'moderate_pos'),
    ('Living_Area', 'Type_of_Property', 'moderate_pos'),
    ('Garden', 'Type_of_Property', 'moderate_pos'),
    ('Number_of_Facades', 'Surface_area_plot_of_land', 'moderate_pos'),
    ('Number_of_Rooms', 'Subtype_of_Property', 'moderate_pos'),
    ('Lift', 'Type_of_Property', 'strong_neg'),  # Strong negative
    ('Lift', 'Subtype_of_Property', 'strong_neg'),
    ('Lift', 'Living_Area', 'moderate_neg'),  # Moderate negative
    ('Lift', 'Number_of_Rooms', 'moderate_neg')
]

color_mapping = {
    'strong_pos': 'green',
    'moderate_pos': 'blue',
    'moderate_neg': 'orange',
    'strong_neg': 'red'
}

# Overlay circles on selected correlations with different colors
ax = plt.gca()  # Get the current axis
for var1, var2, category in highlighted_correlations:
    if var1 in correlation_matrix.columns and var2 in correlation_matrix.columns:
        x = correlation_matrix.columns.get_loc(var1) + 0.5
        y = correlation_matrix.index.get_loc(var2) + 0.5
        circle = plt.Circle((x, y), 0.3, color=color_mapping[category], fill=False, linewidth=2)
        ax.add_artist(circle)

# Adding axes for variables
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Variables", fontsize=12)
plt.ylabel("Variables", fontsize=12)

# Adding a legend for the colors
legend_patches = [
    mpatches.Patch(color=color, label=category.replace('_', ' ').capitalize())
    for category, color in color_mapping.items()
]
plt.legend(
    handles=legend_patches, loc='upper right', bbox_to_anchor=(1.20, 0.05), title="Correlation Type"
)

# Title and layout
plt.title("Correlation Heatmap with Highlighted Relationships", fontsize=16)
plt.tight_layout()

# Render the heatmap in Streamlit
st.pyplot(plt)

# Separate data for houses and apartments
if 'Type_of_Property' in data.columns:
    houses_data = data[data['Type_of_Property'] == 'HOUSE']
    apartments_data = data[data['Type_of_Property'] == 'APARTMENT']
else:
    st.warning("Column 'Type_of_Property' not found in the dataset.")

# Encode categorical columns for both houses and apartments
categorical_columns = data.select_dtypes(include=['object']).columns
encoded_houses_data = houses_data.copy()
encoded_apartments_data = apartments_data.copy()

for column in categorical_columns:
    encoded_houses_data[column] = LabelEncoder().fit_transform(houses_data[column].astype(str))
    encoded_apartments_data[column] = LabelEncoder().fit_transform(apartments_data[column].astype(str))

# Features of interest for correlation analysis
selected_features = ['Swimming_Pool', 'Garden', 'Price', 'Living_Area', 'Number_of_Rooms', 
                     'Fully_Equipped_Kitchen', 'Terrace']

# Compute correlation for Houses
correlation_houses_data = encoded_houses_data[selected_features].corr()

# Compute correlation for Apartments
correlation_apartments_data = encoded_apartments_data[selected_features].corr()

# Function to plot correlation heatmap for houses and apartments
def plot_correlation(correlation_matrix, plot_title):
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar_kws={"shrink": 0.8}
    )
    plt.title(plot_title, fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

# Plot correlation heatmap for Houses
plot_correlation(correlation_houses_data, "Correlation Heatmap for Houses: Features Impact on Price")

# Plot correlation heatmap for Apartments
plot_correlation(correlation_apartments_data, "Correlation Heatmap for Apartments: Features Impact on Price")
