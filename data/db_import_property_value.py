import pandas as pd
import psycopg2


from config.db_config import DB_SETTINGS


# "property_value" data
# Step 1: Read the CSV file into a DataFrame
csv_file_path = 'property_value.csv'
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

# Step 3,4 for "property_value" table
# Step 3: Create a table if it doesn't exist (optional)
create_table_query = '''
CREATE TABLE IF NOT EXISTS campusplastics.property_value (
    id SERIAL PRIMARY KEY,
    property_type_id INTEGER,
    property_name TEXT,
    value_double DOUBLE PRECISION,
    value_text TEXT,
    unit TEXT,
    test_standard TEXT
)
'''
cursor.execute(create_table_query)
conn.commit()

# Step 4: Insert data into the table
for _, row in df.iterrows():
    insert_query = '''
    INSERT INTO campusplastics.property_value (
    property_type_id, property_name, value_double, value_text, unit, test_standard)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        row['property_type_id'], row['property_name'],
        row['value_double'], row['value_text'],
        row['unit'], row['test_standard']
    ))
    conn.commit()

# Step 5: Close the connection
cursor.close()
conn.close()

print("Data imported successfully.")
