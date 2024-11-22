import pandas as pd
import numpy as np

def clean_dataset_with_analysis(file_path, output_path, drop_threshold=0.05):
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

        # Define critical columns that should not be dropped
        critical_columns = ['Price', 'Type_of_Property', 'Locality', 'Number_of_Rooms', 'State_of_the_Building']
        
        # Drop columns with > drop_threshold missing data, excluding critical columns
        threshold = drop_threshold * len(df)
        columns_to_drop = [
            col for col in missing_info[missing_info['Missing Values'] > threshold].index
            if col not in critical_columns
        ]
        print(f"Dropping columns with more than {drop_threshold * 100}% missing data: {columns_to_drop}")
        df = df.drop(columns=columns_to_drop)

        # Drop rows where critical columns have missing values
        df = df.dropna(subset=[col for col in critical_columns if col in df.columns])

        # Fill missing values for categorical data with mode based on grouped data
        def get_grouped_mode(dataframe, group, column):
            mode_dict = dataframe.groupby(group)[column].apply(pd.Series.mode).to_dict()
            return {key: mode_dict[key] for key in mode_dict if not mode_dict[key].empty}
        
        # Handle 'Lift' if it exists in the dataset
        if 'Lift' in df.columns and 'Subtype_of_Property' in df.columns:
            lift_dict = get_grouped_mode(df, 'Subtype_of_Property', 'Lift')
            df['Lift'] = df['Lift'].fillna(df['Subtype_of_Property'].map(lift_dict))
            print(f"Lift grouped mode: {lift_dict}")

        # Price grouping
        price_bins = list(range(0, 300000, 100000)) + \
                     list(range(350000, 1100000, 200000)) + \
                     list(range(1100000, 3000000, 1000000)) + [float('inf')]
        price_labels = [
            f"{price_bins[i]}-{price_bins[i + 1]}" if price_bins[i + 1] != float('inf') else f"{price_bins[i]}+"
            for i in range(len(price_bins) - 1)
        ]
        df['Price_Group'] = pd.cut(df['Price'], bins=price_bins, labels=price_labels, include_lowest=True)

        if 'province' in df.columns:
            df["Price_Group_Per_Region"] = df['province'] + '_' + df["Price_Group"].astype(str)
            if 'State_of_the_Building' in df.columns:
                state_mode_dict = df.groupby('Price_Group_Per_Region')['State_of_the_Building'].apply(
                    lambda x: x.mode().iloc[0] if not x.mode().empty else None
                ).to_dict()
                df["State_of_the_Building"] = df["State_of_the_Building"].fillna(df['Price_Group_Per_Region'].map(state_mode_dict))
        
        # Handle 'Number_of_Facades' based on median grouped by 'Subtype_of_Property'
        if 'Subtype_of_Property' in df.columns and 'Number_of_Facades' in df.columns:
            nb_of_facades_dict = df.groupby('Subtype_of_Property')['Number_of_Facades'].median().to_dict()
            df['Number_of_Facades'] = df['Number_of_Facades'].fillna(df['Subtype_of_Property'].map(nb_of_facades_dict))

        # Replace missing values for 'Surface_area_plot_of_land' with 0
        if 'Surface_area_plot_of_land' in df.columns:
            df['Surface_area_plot_of_land'] = df['Surface_area_plot_of_land'].fillna(0)

        # Fill numerical columns with median
        for col in df.select_dtypes(include=['float64', 'int64']).columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        # Fill categorical columns with mode
        for col in df.select_dtypes(include=['object']).columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mode()[0])
        
        # Remove outliers using IQR
        def remove_outliers(data, columns):
            for col in columns:
                if col in data.columns:
                    Q1 = data[col].quantile(0.25)
                    Q3 = data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
            return data
        
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
        print(f"Removing outliers from columns: {list(numerical_columns)}")
        df = remove_outliers(df, numerical_columns)

        # Save the cleaned dataset
        df.to_csv(output_path, index=False)
        print(f"Cleaned dataset saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
clean_dataset_with_analysis('immoweb_data_city.csv', 'immoweb_data_cleaned_combined.csv')
