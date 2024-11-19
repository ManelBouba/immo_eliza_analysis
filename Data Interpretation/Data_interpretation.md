# 1-cleaning data 
Analysis of Dropped Columns
Open_fire (95.78% missing):
Extremely high missing rate.
Likely contributes minimally to predictions due to the sparsity of data.
Dropping justified.

Garden (77.12% missing):
Very high missing rate.
Likely redundant if Garden_Area (same missing percentage) is also dropped.
Dropping justified.

Surface_of_the_Land (77.12% missing):
Duplicate information with Surface_area_plot_of_land, which has lower missing rates.
Dropping justified.

Garden_Area (77.12% missing):
High missing rate.
Related to Garden, which is also dropped, making it redundant.
Dropping justified.

Swimming_Pool (61.66% missing):
High missing rate.
Limited value unless the model specifically focuses on luxury properties.
Dropping justified.

Terrace_Area (58.27% missing):
High missing rate.
If Terrace is retained, it provides sufficient binary information about its presence.
Dropping justified.

Furnished (54.51% missing):
Moderate missing rate, but its importance depends on whether the dataset focuses on rental or sales listings.
For simplicity in handling missing data, dropping is reasonable.

Disabled_Access (52.75% missing):
Slightly more than half the values are missing.
Likely not critical unless the analysis specifically focuses on accessibility.
Dropping justified.
Retained Columns Analysis
High Missing Rate but Retained

Surface_area_plot_of_land (45.91% missing):
Key quantitative variable for predicting Price.
Imputation techniques (e.g., mean, median) could be applied.

Lift (38.86% missing):
Important for certain property types (e.g., apartments).
Retain and consider imputing missing values.

Terrace (32.36% missing):
Important for property desirability.
Binary encoding simplifies analysis.

Number_of_Facades (29.40% missing):
Architecturally significant and could influence property valuation.
Retain with imputation.

State_of_the_Building (15.56% missing):
Crucial categorical variable for predicting Price.
Missing values can be imputed based on other building characteristics.
Low Missing Rate

Living_Area (3.64% missing):
Highly correlated with Price.
Missing values can be easily imputed.

No Missing Values (Key Variables):
Locality
Price
Subtype_of_Property
Type_of_Property
Number_of_Rooms
Fully_Equipped_Kitchen

Conclusion: Justification for Dropping
Dropping the columns Open_fire, Garden, Surface_of_the_Land, Garden_Area, Swimming_Pool, Terrace_Area, Furnished, Disabled_Access is appropriate because:
They have high missing value percentages.
Their contribution to predictive power is minimal given available data.
They could introduce unnecessary noise into the model.

# 2-Correlation Heatmap with Price

| Feature                    | Correlation with Price | Interpretation                                                                                             |
|----------------------------|------------------------|-----------------------------------------------------------------------------------------------------------|
| Price                      | 1.0                    | Perfect correlation with itself                                                                            |
| Living_Area                | 0.424615               | Moderate positive correlation. Larger living areas tend to lead to higher prices.                          |
| Number_of_Rooms            | 0.364242               | Moderate positive correlation. More rooms tend to result in higher prices.                                |
| Fully_Equipped_Kitchen     | 0.212158               | Weak positive correlation. A fully equipped kitchen adds value but not a major factor.                    |
| Surface_area_plot_of_land  | 0.191891               | Weak positive correlation. Larger land plots tend to slightly increase the price.                         |
| Subtype_of_Property        | 0.164309               | Weak positive correlation. Some property types (e.g., villas) tend to be priced higher.                  |
| Number_of_Facades          | 0.157504               | Weak positive correlation. More facades may indicate a larger or more prestigious property.               |
| Type_of_Property           | 0.101701               | Very weak positive correlation. The property type doesn't have a strong impact on price.                  |
| Lift                       | 0.025784               | Very weak positive correlation. The presence of a lift/elevator has minimal impact on price.               |
| Locality                   | -0.006981              | No significant correlation. Locality may be important but is not well captured in this dataset.            |
| State_of_the_Building      | -0.136933              | Weak negative correlation. Older or poorly maintained buildings may have a slightly lower price.           |
| Terrace                    |                        | No correlation due to missing data or lack of variation. Needs cleaning or re-encoding.                    |
1. Key Positive Correlations with Price
Living_Area (0.42):

A significant positive correlation with Price. Larger living areas tend to increase the price.
Number_of_Rooms (0.36):

A positive correlation. Homes with more rooms are generally more expensive.
Fully_Equipped_Kitchen (0.21):

A moderately positive correlation. Houses with fully equipped kitchens tend to have a higher price.
Surface_area_plot_of_land (0.19):

A smaller but still positive correlation. Larger land plots slightly increase the price.
Number_of_Facades (0.16):

A weaker positive correlation. The architectural feature (number of facades) slightly impacts the price.
2. Key Negative Correlations with Price
State_of_the_Building (-0.14):
A weak negative correlation. Older or poorly maintained buildings reduce the price slightly.
Lift (0.02):
Almost no meaningful correlation between Lift and Price, suggesting that its presence might not impact property value directly.

# 3-Correlation Heatmap of variables
Highly Correlated Variables
Type_of_Property and Subtype_of_Property (0.69):

This is the strongest correlation in the dataset. It reflects the natural hierarchical relationship: subtypes (e.g., villa, apartment) are more specific classifications of property types (e.g., house, flat).
Living_Area and Number_of_Rooms (0.54):

Larger living areas are associated with more rooms, which makes intuitive sense for residential properties.
Number_of_Rooms and Type_of_Property (0.50):

Property types influence the number of rooms. For instance, houses generally have more rooms than apartments.
Living_Area and Type_of_Property (0.40):

Larger living areas are more common in specific property types (e.g., houses vs. apartments).
Subtype_of_Property and Number_of_Facades (0.33):

The subtype of a property affects the number of facades (e.g., detached homes are more likely to have multiple facades compared to apartments).
2. Moderately Correlated Variables
Surface_area_plot_of_land and Living_Area (0.26):

Larger living areas tend to come with larger land plots, though this is not always true (e.g., high-rise apartments with large living areas).
Surface_area_plot_of_land and Number_of_Facades (0.20):

More facades are slightly associated with larger land plots, likely reflecting detached homes with more surrounding space.
State_of_the_Building and Fully_Equipped_Kitchen (-0.26):

Better-maintained buildings are more likely to have fully equipped kitchens. This suggests that property condition is related to its features.
Number_of_Facades and Number_of_Rooms (0.24):

More facades slightly indicate properties with more rooms, reflecting larger, detached homes.
3. Weakly Correlated Variables
Living_Area and Fully_Equipped_Kitchen (0.03):

The size of the living area has almost no impact on whether the property has a fully equipped kitchen.
Locality with most variables:

Correlations involving Locality are weak or negligible, suggesting that the dataset may not capture meaningful geographic variation. Geographic grouping could provide more insights.
Lift with other variables:

Most correlations with Lift are weak. The strongest negative correlation is with Type_of_Property (-0.67), likely reflecting that lifts are predominantly in apartments rather than detached homes.
4. Key Takeaways
Subtype_of_Property: This variable strongly influences others, such as Type_of_Property, Number_of_Rooms, and Number_of_Facades.
Living_Area: Correlates strongly with Number_of_Rooms and moderately with Surface_area_plot_of_land. This makes it an essential factor in determining property characteristics.
Type_of_Property: Influences multiple variables, including Subtype_of_Property, Number_of_Rooms, and Living_Area.
Locality: Has limited impact on other variables in this dataset, suggesting it might be better analyzed through clustering or geospatial analysis.
# 4_the greatest and the least influence on the price:
Greatest Influence: Living_Area, Number_of_Rooms, Fully_Equipped_Kitchen.
Least Influence: Lift, Locality, Type_of_Property.
# 5-count of Qualitative and Quantitative Variables

Quantitative Variables:
These are numerical variables directly usable in analysis:
Price
Number_of_Rooms
Living_Area
Surface_area_plot_of_land
Number_of_Facades
Count: 5 

Qualitative Variables:
These are categorical variables requiring transformation:
Locality
Type_of_Property
Subtype_of_Property
State_of_the_Building
Fully_Equipped_Kitchen (binary: yes/no)
Terrace (binary: yes/no)
Lift (binary: yes/no)
Count: 7 qualitative variables 