import pandas as pd

file = pd.read_csv('immoweb_data.csv')

df = pd.DataFrame(file)
import numpy as np

#Keep (core) ['Price', 'Locality','Living_Area','Number_of_Rooms','Subtype_of_Property']
#Drop ['Open_fire', 'Garden_Area', 'Terrace_Area', 'Swimming_Pool', 'Disabled_Access']
#Replace from other entries [Lift, State_of_the_Building, Number_of_Facades]

'''
Remove: 1 open fire -> too many missing entries too little meaning
        2 Garden Area -> too many missing entries, not as meaningful as knowing if there is a garden
        3 Terrace Area -> // // // terrace
        5 Disabled Access -> Too difficult if not impossible to deduct and too many missing entries

Keep: All the core columns
      Maybe keep
      4 Swimming Pool -> Too many missing values, too difficult to deduct from other columns, makes sense as this is a general property market and not luxury estate one
Fill: 1 Lift can be defaulted to 0 for subtype property House (majorit of entries) and deducted for other types
      2 State of the building, very important factor in determining price of a property, can be deducted by price and locality
      3 Garden, many missing entries but very determining in price and it's unlikely they forgot to add to the property listing -> can be defaulted to 0
      4 Terrace, same as garden
      5 Number of Facades, on the fence about this, but can be defaulted to 1 for apartments
'''

core_columns = ['Price', 'Locality','Living_Area','Number_of_Rooms','Subtype_of_Property']

threshold = len(df) * 0.05

colums_to_drop_low_meaning = ['Open_fire', 'Garden_Area', 'Terrace_Area', 'Swimming_Pool', 'Disabled_Access','Surface_of_the_Land','Furnished']

df.drop(colums_to_drop_low_meaning, axis=1,inplace=True)
columns_low_entries = df.columns[df.isna().sum() < threshold]
df.dropna(subset=columns_low_entries, inplace=True)
df[['Garden','Terrace']] = df[['Garden','Terrace']].fillna(0)

def get_grouped_mode(dataframe, group, column):
   mode_dict = dataframe.groupby(group)[column].apply(pd.Series.mode).to_dict()
   parsed_mode_dict = {key[0]: mode_dict[key] for key in mode_dict.keys()}
   return parsed_mode_dict

lift_dict = get_grouped_mode(df,'Subtype_of_Property', 'Lift')
df["Lift"] = df["Lift"].fillna(df["Subtype_of_Property"].map(lift_dict))
print(lift_dict)

#Create new column for price ranges
price_bins = [i* 100000 for i in range(0,11)]
price_bins += [i* 1000000 for i in range(2,15)]
#Create labels for each range
price_labels = [f"{(i - 1)*100}-{i *100}k" for i in range(1,10)]
price_labels += ["950k-1M"]
price_labels += [f"{i-1}-{i}M" for i in range(2,15)]

df['Price_Bin'] = pd.cut(df['Price'], bins=price_bins, labels=price_labels)


state_of_building_dict = get_grouped_mode(df,['Price_Bin','Locality'], 'State_of_the_Building')
# print(df.groupby(["Locality","Price_Bin"])["State_of_the_Building"].apply(pd.Series.mode))
print(df.pivot_table(values="State_of_the_Building",index="Locality", columns="Price_Bin", aggfunc=pd.Series.mode))
# df["State_of_the_Building"] = df["State_of_the_Building"].fillna(df['Locality','Price_Bin'].map(state_of_building_dict))
#Todo pass mode of two different columns
#Maybe not good idea for since the key value pairs would be too unique?
# lift_dict = df.groupby(['Subtype_of_Property'])["Lift"].agg(pd.Series.mode)
percent_missing = df.isnull().sum() * 100 / len(df)
missing_value_df = pd.DataFrame({'column_name': df.columns,
                                 'percent_missing': percent_missing})
print(missing_value_df.sort_values(by="percent_missing", ascending=False))


