import pandas as pd
import numpy as np

"""
Step 1: Split 'Value' column into 'value_double' and 'value_text'
Step 2: Add 'property_type_ids' column
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
property_columns = ['Rheological properties', 'Mechanical properties',
                    'Thermal properties', 'Electrical properties',
                    'Other properties']

def determine_property_type_id(row):
    for i, col in enumerate(property_columns):
        if pd.notnull(row[col]):
            return i + 1
    return np.nan

df['property_type_id'] = df.apply(determine_property_type_id, axis=1)

# Step 3: Unite all property columns into "property_name"
df['property_name'] = df[property_columns].bfill(axis=1).iloc[:, 0]

# Drop the original property columns
df.drop(columns=property_columns, inplace=True)
df.drop(columns=['Value'], inplace=True)

# Step 4: Rename the columns
df.rename(columns={
    'Unit': 'unit',
    'Test Standard': 'test_standard'
}, inplace=True)

# Save the modified DataFrame to a new CSV file
df.to_csv('transformed.csv', index=False)

print("CSV file created successfully with the specified modifications.")
