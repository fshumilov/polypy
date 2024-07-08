import pandas as pd
import psycopg2


from config.db_config import DB_SETTINGS


# Step 1: Read the CSV file into a DataFrame
csv_file_path = 'property_type.csv'
df_property_type = pd.read_csv(csv_file_path)

# Step 2: Connect to PostgreSQL database
conn = psycopg2.connect(
    host=DB_SETTINGS['host'],
    database=DB_SETTINGS['database'],
    user=DB_SETTINGS['user'],
    password=DB_SETTINGS['password'],
    port=DB_SETTINGS['port_id']
)
cursor = conn.cursor()

# Step 3,4 for "property_type" table
# Step 3: Create a table if it doesn't exist (optional)
create_table_query = '''
CREATE TABLE IF NOT EXISTS campusplastics.property_type (
    id SERIAL PRIMARY KEY,
    polymer_catalog_id INTEGER,
    property_type TEXT
)
'''
cursor.execute(create_table_query)
conn.commit()

# Step 4: Insert data into the table
for _, row in df_property_type.iterrows():
    insert_query = '''
    INSERT INTO campusplastics.property_type(
    polymer_catalog_id, property_type)
    VALUES (%s, %s)
    '''
    cursor.execute(insert_query, (
        row['polymer_catalog_id'], row['property_type']
    ))
    conn.commit()

# Step 5: Close the connection
cursor.close()
conn.close()

print("Data imported successfully.")
