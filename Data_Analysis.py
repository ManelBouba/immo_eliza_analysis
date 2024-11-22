# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from scipy.stats import chi2_contingency, f_oneway, pointbiserialr

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
    print("Top Localities by Average Price:")
    print(locality_agg.sort_values(by='Average_Price', ascending=False).head())

# Step 4: Separate numeric and categorical columns
numeric_cols = data.select_dtypes(include=['number']).columns
categorical_cols = data.select_dtypes(include=['object']).columns

print(f"Numeric columns: {numeric_cols}")
print(f"Categorical columns: {categorical_cols}")

# Step 5: Encode categorical columns for correlation analysis
label_encoder = LabelEncoder()
encoded_data = data.copy()
for col in categorical_cols:
    encoded_data[col] = label_encoder.fit_transform(data[col].astype(str))

# Step 6: Compute correlation matrix
correlation_matrix = encoded_data.corr()

# Step 7: Display correlation with target variable 'Price'
if 'Price' in correlation_matrix.columns:  # Check to ensure 'Price' exists
    print("\nCorrelation of all variables with 'Price':")
    print(correlation_matrix["Price"].sort_values(ascending=False))

    # Visualization: Correlation Heatmap with Price
    plt.figure(figsize=(10, 6))
    sns.heatmap(
        correlation_matrix["Price"].sort_values(ascending=False).to_frame(),
        annot=True, cmap="coolwarm", fmt=".2f", cbar_kws={"shrink": 0.8}
    )
    plt.title("Correlation of Variables with Price")
    plt.tight_layout()
    plt.show()

# Visualization: Full Correlation Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar_kws={"shrink": 0.8})
plt.title("Correlation Heatmap (Including Encoded Categorical Variables)")
plt.tight_layout()
plt.show()

