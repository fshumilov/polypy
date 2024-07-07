import pandas as pd
import numpy as np


from parser import property_names
from property_type_df import polymer_catalog_id
from models.db_requests import get_property_type

"""
Step 1: Split 'Value' column into 'value_double' and 'value_text'
Step 2: Add 'property_type_ids' column 
        according to a polymer_catalog_id and ids from the property_type table
Step 3: Unite all property columns into "property_name" and remove "Value" column
Step 4: Rename "Unit" to "unit" and "Test Standard" to "test_standard"
"""

# Load the CSV file
df = pd.read_csv('parsed.csv')


# Step 1: Split 'Value' column into 'value_double' and 'value_text'
def identify_type(value):
    try:
        return float(value)
    except ValueError:
        return value


df['identified_value'] = df['Value'].apply(identify_type)

df['value_double'] = pd.to_numeric(df['identified_value'], errors='coerce')
df['value_text'] = df['identified_value'].apply(lambda x: x if isinstance(x, str) else np.nan)

# Drop the intermediate 'identified_value' column
df.drop(columns=['identified_value'], inplace=True)


# Step 2: Add 'property_type_ids' column
# form a df from id and property_type of the property_type table
df_property_type = get_property_type()
filtered_df = pd.DataFrame(
    df_property_type.loc[df_property_type['polymer_catalog_id'] == polymer_catalog_id]
)

# Initialize the property_type_id column with NaN values
df['property_type_id'] = None


# Rename columns names from "xxx properties" to "xxx"
# Function to rename columns
def rename_columns(columns):
    return {col: col.replace(' properties', '') for col in columns}


# Applying the function to the DataFrame
new_column_names = rename_columns(df.columns)
df.rename(columns=new_column_names, inplace=True)

# Iterate through the columns of df
for col in df.columns[:-1]:  # Exclude the 'property_type_id' column
    if col in filtered_df['property_type'].values:
        # Get the id corresponding to the property_type
        prop_id = filtered_df.loc[filtered_df['property_type'] == col, 'id'].values[0]

        # If the column contains non-NaN values, set the property_type_id
        df.loc[df[col].notna(), 'property_type_id'] = prop_id


# Step 3: Unite all property columns into "property_name"
split_property_names = [item.split()[0] for item in property_names]
df['property_name'] = df[split_property_names].bfill(axis=1).iloc[:, 0]

# Drop the original property columns
df.drop(columns=split_property_names, inplace=True)
df.drop(columns=['Value'], inplace=True)


# Step 4: Rename the columns
df.rename(columns={
    'Unit': 'unit',
    'Test Standard': 'test_standard'
}, inplace=True)

# Save the modified DataFrame to a new CSV file
df.to_csv('property_value.csv', index=False)

print("CSV file created successfully with the specified modifications.")
