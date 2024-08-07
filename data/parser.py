import logging
import pandas as pd
from bs4 import BeautifulSoup


"""
1) Load and parse the HTML file.
2) Find all relevant div blocks.
3) Iterate over each div block and extract tables within them.
4) Extract headers and rows from each table.
5) Store the extracted data in a structured format.
6) Print or save the data to a CSV file.
"""

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)
# Set the logging group
log_parser = logging.getLogger("parser")

# Load the HTML content from the file
file_path = '3.html'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title of the page
page_title = soup.title.string if soup.title else "No title found"
log_parser.debug(f"Page Title: {page_title}")
# Splitting the title
words_list = str(page_title).split()
split_page_title = ' '.join(words_list[3:])
page_title = split_page_title
log_parser.info(f'Polymer title: {page_title}')

# Extract the polymer name into the .csv file to import
df_page_title = pd.DataFrame([str(page_title)], columns=['polymer_name'])
df_page_title.to_csv('polymer_title.csv', index=False)

# Find all relevant div blocks
div_blocks = soup.find_all('div', class_='group groupspt')

# Initialize a list to store all table data
all_table_data = []
all_data = []  # data without headers

# Iterate over each div block
for div in div_blocks:
    # Find all tables within the div block
    tables = div.find_all('table', class_='full')

    # Iterate over each table
    for table in tables:
        table_data = []
        # Find all rows in the table
        rows = table.find_all('tr')

        # Extract headers
        header_row = rows[0]  # assuming the first row is the header
        header_columns = header_row.find_all(['th', 'td'])  # headers might be in 'th' or 'td'
        headers = [header.text.strip() for header in header_columns]

        # Extract data rows
        for row in rows[1:]:  # skipping the header row
            columns = row.find_all('td')
            if len(columns) == len(headers):
                row_data = {headers[i]: columns[i].text.strip() for i in range(len(headers))}
                table_data.append(row_data)

        # Append the extracted table data to all_table_data
        all_table_data.append((headers, table_data))
        all_data.append(table_data)  # it's a list of lists with dictionaries

log_parser.debug(f"There is a 'all_table_data' - data with headers: {all_table_data}")
log_parser.debug(f"There is a 'all_table_data' - data WITHOUT headers: {all_data}")
log_parser.debug("Data type of 'all_data' is a list of lists with dictionaries")

# Flatten the list of lists
flattened_data = [item for sublist in all_data for item in sublist]

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(flattened_data)

# Save DataFrame to CSV
df.to_csv('parsed.csv', index=False)

# for "property_type"
# Initialize a list to store all table data
property_names = []  # to use it in a property_type table

# Print all table data
for index, (headers, table_data) in enumerate(all_table_data):
    # print(f"\nTable {index + 1}:")
    # print(headers)
    property_names.append(headers[0])
    # for row in table_data:
    #     print(row)

log_parser.info(f"List of property names: {property_names}")

# Save property_names as a dataframe
df_property_names = pd.DataFrame(property_names, columns=['property_name'])
df_property_names.to_csv('property_names.csv', index=False)

# # Save each table in a separate CSV file
# for index, (headers, table_data) in enumerate(all_table_data):
#     csv_file_path = f'table_{index + 1}.csv'
#     with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#         writer = csv.DictWriter(csv_file, fieldnames=headers)
#         writer.writeheader()
#         writer.writerows(table_data)
#     print(f"Table {index + 1} saved to {csv_file_path}")
