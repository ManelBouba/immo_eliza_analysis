# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Set visualization style
sns.set_style("whitegrid")

# Load the data
data = pd.read_csv("immoweb_data_cleaned.csv")

# Preview the data
print(data.head())
print(data.info())
print(data.describe())

# Check for missing values
print(data.isnull().sum())

# Combined function to compute and plot two heatmaps: 1) with price, 2) between variables
def compute_and_plot_heatmaps(data, target_column='Price', output_csv_file='correlation_results.csv'):
    
    if target_column not in data.columns:
        print(f"Error: '{target_column}' not found in the dataset.")
        return
    
    # Separate numeric and object (categorical) columns
    numeric_data = data.select_dtypes(include=['number'])
    object_data = data.select_dtypes(include=['object'])
    
    # Convert object columns to numeric using label encoding for correlation purposes
    label_encoder = LabelEncoder()
    for col in object_data.columns:
        data[col] = label_encoder.fit_transform(data[col].astype(str))
    
    # Compute the correlation matrix for all variables
    correlation_matrix = data.corr()
    
    # Extract correlation with respect to the target column
    target_correlation = correlation_matrix[target_column].sort_values(ascending=False)
    
    # Print the correlation with the target column
    print(f"\nCorrelation with {target_column}:\n", target_correlation)
    
    # Save the correlation results with respect to the target column to a CSV file
    target_correlation.to_frame().drop(target_column, axis=0).to_csv(output_csv_file)
    
    # Plot: Heatmap of correlation with the target variable (e.g., 'Price')
    plt.figure(figsize=(10, 6))  # Set size for better visibility
    sns.heatmap(
        target_correlation.to_frame().drop(target_column, axis=0).T, 
        annot=True,               # Annotate cells with correlation values
        cmap="coolwarm",          # Color scheme for the heatmap
        fmt=".2f",                # Format the numbers to two decimal places
        annot_kws={"size": 12},   # Font size for annotations
        cbar_kws={'shrink': 0.8}  # Adjust the color bar size
    )
    plt.title(f"Correlation of Variables with {target_column}", fontsize=16)
    plt.tight_layout()
    plt.show()
    
    # Plot: Heatmap of correlation between all numeric variables
    plt.figure(figsize=(12, 8))  # Set size for better visibility
    sns.heatmap(
        correlation_matrix, 
        annot=True,               # Annotate cells with correlation values
        cmap="coolwarm",          # Color scheme for the heatmap
        fmt=".2f",                # Format the numbers to two decimal places
        annot_kws={"size": 12},   # Font size for annotations
        cbar_kws={'shrink': 0.8}  # Adjust the color bar size
    )
    plt.title("Correlation Heatmap of All Numeric Variables", fontsize=16)
    plt.tight_layout()
    plt.show()

    # Save the full correlation matrix to a CSV file
    correlation_matrix.to_csv('full_correlation_matrix.csv')

# Example usage:
compute_and_plot_heatmaps(data, target_column='Price', output_csv_file='correlation_with_price.csv')
