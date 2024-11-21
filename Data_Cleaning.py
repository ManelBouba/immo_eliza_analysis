import pandas as pd


def clean_dataset_with_analysis(file_path, output_path, drop_threshold=0.5):
  
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        
        # Analyze missing values
        print("Analyzing missing values...")
        missing_data = df.isnull().sum()
        missing_percentage = (missing_data / len(df)) * 100
        missing_info = pd.DataFrame({
            'Missing Values': missing_data,
            'Percentage': missing_percentage
        }).sort_values(by='Percentage', ascending=False)
        print(missing_info)
        
        # Drop columns with > drop_threshold missing data
        threshold = drop_threshold * len(df)
        columns_to_drop = missing_info[missing_info['Missing Values'] > threshold].index
        print(f"Dropping columns: {list(columns_to_drop)}")
        df = df.drop(columns=columns_to_drop)
        
        # Drop rows where critical columns have missing values
        critical_columns = ['Price', 'Type_of_Property', 'Locality']
        df = df.dropna(subset=critical_columns)
        
        # Fill missing values
        for col in df.select_dtypes(include=['float64', 'int64']).columns:
            df[col] = df[col].fillna(df[col].median())  # Median for numerical columns
        
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].fillna(df[col].mode()[0])  # Mode for categorical columns
        
        # Save the cleaned dataset
        df.to_csv(output_path, index=False)
        print(f"Cleaned dataset saved to {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
clean_dataset_with_analysis('apartment_dataset.csv', 'immoweb_data_appartment_cleaned.csv') # for appartment
clean_dataset_with_analysis('houses_dataset.csv', 'immoweb_data_houses_cleaned.csv') # for houses

