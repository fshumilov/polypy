import pandas as pd
import psycopg2


from config import DB_SETTINGS

# Step 1: Read the CSV file into a DataFrame
csv_file_path = 'transformed.csv'
df = pd.read_csv(csv_file_path)

# Step 2: Connect to PostgreSQL database
conn = psycopg2.connect(
    host=DB_SETTINGS['host'],
    database=DB_SETTINGS['database'],
    user=DB_SETTINGS['user'],
    password=DB_SETTINGS['password'],
    port=DB_SETTINGS['port_id']
)
cursor = conn.cursor()

# Step 3: Create a table if it doesn't exist (optional)
create_table_query = '''
CREATE TABLE IF NOT EXISTS campusplastics.property_value (
    id SERIAL PRIMARY KEY,
    value_double DOUBLE PRECISION,
    value_text TEXT,
    property_type_ids INTEGER,
    property_name TEXT
)
'''
cursor.execute(create_table_query)
conn.commit()

# Step 4: Insert data into the table
for _, row in df.iterrows():
    insert_query = '''
    INSERT INTO property_value (value_double, value_text, property_type_ids, property_name)
    VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (row['value_double'], row['value_text'], row['property_type_ids'], row['property_name']))
    conn.commit()

# Step 5: Close the connection
cursor.close()
conn.close()

print("Data imported successfully.")
