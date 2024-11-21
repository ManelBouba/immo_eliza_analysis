import pandas as pd
import numpy as np

def clean_dataset_with_analysis(file_path, output_path, drop_threshold=0.05):
  
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        # Drop columns with > drop_threshold missing data
        threshold = drop_threshold * len(df)
        columns_to_drop = ['Open_fire', 'Garden_Area', 'Terrace_Area', 'Disabled_Access','Surface_of_the_Land','Furnished']
        df = df.drop(columns=columns_to_drop)
        columns_low_missing_data = df.columns[df.isna().sum() < threshold]
        df.dropna(subset=columns_low_missing_data, inplace=True)
        
        
        # Fill missing values with defaults
        df[['Garden','Terrace','Swimming_Pool']] = df[['Garden','Terrace','Swimming_Pool']].fillna(0)
        
        #Fill missing values for categorical data with mode based on similar entries by grouped data
        lift_dict = get_grouped_mode(df,'Subtype_of_Property', 'Lift')
        df["Lift"] = df["Lift"].fillna(df["Subtype_of_Property"].map(lift_dict))
        print(lift_dict)

        #Categorize municipalities into provinces:
        provinces = ['Brussels Capital','Walloon Brabant', 'Flemish Brabant', 'Antwerp', 'Limburg','Liège','Namur','Hainaut','Luxembourg','West Flanders','East Flanders']
        brussels_capital = r'^10|^11|^12'
        walloon_brabant = r'^13|^14'
        flemish_brabant = r'^15|^16|^17|^18|^19|^30|^31|^32|^34'
        antwerp = r'^20|^21|^22|^23|^24|^25|^26|^27|^28|^29'
        limburg = r'^35|^36|^37|^38|^39'
        liège = r'^40|^41|^44|^43|^44|^45|^46|^47|^48|^49'
        namur = r'^50|^51|^55|^53|^55|^55|^56|^57|^58|^59'
        hainaut = r'^60|^61|^62|63|^64|^65|^70|^71|^77|^73|^74|^75|^76|^77|^78|^79'
        luxembourg = r'^66|^67|^68|^69'
        west_flanders = r'^70|^71|^72|^73|^74|^75|^76|^77|^78|^79'
        east_flanders = r'^90|^91|^92|^93|^94|^95|^96|^97|^98|^99'
        conditions = [
        (df["Locality"].astype(str).str.contains(brussels_capital)),
        (df["Locality"].astype(str).str.contains(walloon_brabant)),
        (df["Locality"].astype(str).str.contains(flemish_brabant)),
        (df["Locality"].astype(str).str.contains(antwerp)),
        (df["Locality"].astype(str).str.contains(limburg)),
        (df["Locality"].astype(str).str.contains(liège)),
        (df["Locality"].astype(str).str.contains(namur)),
        (df["Locality"].astype(str).str.contains(hainaut)),
        (df["Locality"].astype(str).str.contains(luxembourg)),
        (df["Locality"].astype(str).str.contains(west_flanders)),
        (df["Locality"].astype(str).str.contains(east_flanders)),
        ]

        df["Province"] = np.select(conditions,provinces, default='Other')

        regions = ['Bruxelles-Capital','Wallonia','Flanders']
        brussels_capital = r'Brussels Capital'
        flanders = r'Flemish Brabant|Antwerp|West Flanders|East Flanders'
        wallonia = r'Walloon Brabant|Limburg|Liège|Namur|Hainaut|Luxembourg'
        conditions = [
        (df["Province"].astype(str).str.contains(brussels_capital)),
        (df["Province"].astype(str).str.contains(wallonia)),
        (df["Province"].astype(str).str.contains(flanders))
        ]

        df["Region"] = np.select(conditions,regions, default='Other')



        price_bins = list(range(0, 300000, 100000))  
        price_bins += list(range(350000, 1100000, 2000000)) 
        price_bins += list(range(1100000, 3000000, 1000000)) 
        price_bins += [float('inf')]  

        price_labels = [
            f"{price_bins[i]}-{price_bins[i + 1]}" if price_bins[i + 1] != float('inf') else f"{price_bins[i]}+"
            for i in range(len(price_bins) - 1)
        ]

        df['Price_Group'] = pd.cut(df['Price'], bins=price_bins, labels=price_labels, include_lowest=True)
        df["Price_Group_Per_Region"] = df['Province'] + '_' +df["Price_Group"].astype(str)
        state_mode_dict = df.groupby('Price_Group_Per_Region')['State_of_the_Building'].apply(
            lambda x: x.mode().iloc[0] if not x.mode().empty else None
        ).to_dict()
        
        size_bins = [0,50,100,200,300]
        size_bins_labels = ["Small","Medium","Large","Very Large"]

        df["Property_Size"] = pd.cut(df['Living_Area'],bins=size_bins,labels=size_bins_labels)

        df["State_of_the_Building"] = df["State_of_the_Building"].fillna(df['Price_Group_Per_Region'].map(state_mode_dict))

        nb_of_facades_dict = df.groupby('Subtype_of_Property')['Number_of_Facades'].median().to_dict()
        df["Number_of_Facades"] = df["Number_of_Facades"].fillna(df['Subtype_of_Property'].map(nb_of_facades_dict))

        df['Surface_area_plot_of_land'] = df['Surface_area_plot_of_land'].fillna(0)

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
        
        numerical_columns = ['Price','Number_of_Rooms','Living_Area','Surface_area_plot_of_land']
        print(f"Removing outliers from columns: {list(numerical_columns)}")
        df = remove_outliers(df, numerical_columns)

        df.drop(['Price_Group','Price_Group_Per_Region'], axis=1, inplace=True)
        #Removing outliers:
        print(df.describe())
        # # Save the cleaned dataset
        df.to_csv(output_path, index=False)
               # Analyze missing values
        print("Analyzing missing values...")
        missing_data = df.isnull().sum()
        missing_percentage = (missing_data / len(df)) * 100
        missing_info = pd.DataFrame({
            'Missing Values': missing_data,
            'Percentage': missing_percentage
        }).sort_values(by='Percentage', ascending=False)
        print(missing_info)

        print(f"Cleaned dataset saved to {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def get_grouped_mode(dataframe, group, column):
   mode_dict = dataframe.groupby(group)[column].apply(pd.Series.mode).to_dict()
   parsed_mode_dict = {key[0]: mode_dict[key] for key in mode_dict.keys()}
   return parsed_mode_dict
# Example usage:
clean_dataset_with_analysis('immoweb_data.csv', 'immoweb_data_cleaned.csv')