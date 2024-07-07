import pandas as pd
import psycopg2


from config.db_config import DB_SETTINGS

# "polymer_catalog" data
# Step 1: Read the CSV file into a DataFrame
csv_file_path = 'polymer_title.csv'
df_polymer_catalog = pd.read_csv(csv_file_path)

# Step 2: Connect to PostgreSQL database
conn = psycopg2.connect(
    host=DB_SETTINGS['host'],
    database=DB_SETTINGS['database'],
    user=DB_SETTINGS['user'],
    password=DB_SETTINGS['password'],
    port=DB_SETTINGS['port_id']
)
cursor = conn.cursor()

# Step 3,4 for "polymer_catalog" table
# Step 3: Create a table if it doesn't exist (optional)
create_table_query = '''
CREATE TABLE IF NOT EXISTS campusplastics.polymer_catalog (
    id SERIAL PRIMARY KEY,
    polymer_name TEXT
)
'''
cursor.execute(create_table_query)
conn.commit()

# Step 4: Insert data into the table
for _, row in df_polymer_catalog.iterrows():
    insert_query = '''
    INSERT INTO campusplastics.polymer_catalog(
    polymer_name)
    VALUES (%s)
    '''
    cursor.execute(insert_query, (
        row['polymer_name'],
    ))
    conn.commit()

# Step 5: Close the connection
cursor.close()
conn.close()

print("Data imported successfully.")