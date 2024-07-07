import pandas as pd

from models.db_requests import get_polymer_catalog
from parser import page_title
from parser import property_names  # Step 1

"""
Step 1: Get a the list of property_names
Step 2: Get a ID value for the polymer title from db
Step 3: Form a data frame from property_names and the polymer title ID
Step 4: Export the data frame into csv file
"""

# Step 2: Get a ID value for the polymer title from db
df_catalog = get_polymer_catalog()
filtered_df = pd.DataFrame(
    df_catalog.loc[df_catalog['polymer_name'] == str(page_title)]
)
polymer_catalog_id = int(filtered_df['id'].iloc[0])

# Step 3: Form a data frame from property_names and the polymer title ID
list_length = len(property_names)
split_property_names = [item.split()[0] for item in property_names]
polymer_title_id_list = [polymer_catalog_id] * list_length

df = pd.DataFrame({
    'polymer_catalog_id': polymer_title_id_list,
    'property_type': split_property_names
})

# Step 4: Save the formed DataFrame to a new CSV file
df.to_csv('property_type.csv', index=False)

print("CSV file to import into the property_type table is created.")
