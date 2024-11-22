#  Data cleaning
# 1

When we drop rows with NaN values, retaining only 49 rows out of 24,000 suggests that your dataset has a high percentage of missing values. This indicates that dropping all NaN values may not be the best approach because it results in a significant loss of data. 
# 2

Our data clearly shows that some columns (e.g., Open_fire, Garden, Surface_of_the_Land) have an extremely high percentage of missing values, while others (e.g., Locality, Price, Type_of_Property) are fully complete. A targeted cleaning approach is essential to minimize data loss while retaining valuable information.

# 3 Decide on Columns to Drop or Keep

Drop Columns with Excessive Missing Data:

Columns with more than 50% missing data might not be useful unless they are critical. For instance, Open_fire, Garden, Surface_of_the_Land, Garden_Area, and Swimming_Pool are candidates for removal.
Customize this threshold if certain columns are important for your analysis.
Retain Key Columns:

Columns like Price, Locality, Type_of_Property, and Subtype_of_Property are critical and must be retained since they have no missing values
# 4 Handle Missing Values in Remaining Columns

For columns with missing values but below the 50% threshold:

Numerical Columns: Impute missing values with the median to avoid distortion by outliers. Examples include Living_Area, Terrace_Area, and Number_of_Facades.

Categorical Columns: Impute missing values with the mode (most frequent value). Examples include State_of_the_Building and Furnished.
For columns with very few missing values (e.g., Living_Area has 3.64%), you might choose to drop the rows instead of imputing.

# 5 Expected Output

Columns like Open_fire and Garden will be removed because they exceed the threshold of 50% missing values.
Missing values in numeric columns like Living_Area and Terrace_Area will be filled with their median values.
Missing values in categorical columns like State_of_the_Building will be filled with their mode (most frequent value).
Rows with missing values in Price, Type_of_Property, and Locality will be dropped, as these are critical.

#  Data Analysis

# 1 correlation 
To determine the correlation between variables and the Price, we can calculate the Pearson correlation coefficient for numerical variables and analyze the relationships for categorical variables.
  # a) Analyze Correlation
   # Numerical Variables
Use the Pearson correlation coefficient to measure linear relationships between Price and other numerical features (e.g., Living_Area, Number_of_Rooms).
A coefficient close to:
1 indicates a strong positive correlation (as one increases, the other increases).
-1 indicates a strong negative correlation (as one increases, the other decreases).
0 indicates no linear correlation.
   # Categorical Variables
Convert categorical variables (e.g., Type_of_Property, Furnished) into numerical representations (e.g., one-hot encoding or label encoding).

  # b) Compute correlation or assess their impact using advanced techniques like:
Mean Price grouped by each category.
ANOVA or chi-squared tests.

Correlation Matrix: Quantifies the relationship between all variables, including encoded categorical ones, with Price.
Chi-Square Test: Identifies significant associations between categorical variables and Price.
Point-Biserial Correlation: Highlights relationships between binary categorical variables and Price.
ANOVA: Assesses the influence of multi-level categorical variables on Price.
Box Plots: Visual representation of the distribution of Price across different categories.