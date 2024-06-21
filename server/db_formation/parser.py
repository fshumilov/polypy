import pandas as pd
from bs4 import BeautifulSoup
import csv

"""
1) Load and parse the HTML file.
2) Find all relevant div blocks.
3) Iterate over each div block and extract tables within them.
4) Extract headers and rows from each table.
5) Store the extracted data in a structured format.
6) Print or save the data to a CSV file.
"""

# Load the HTML content from the file
file_path = 'downloaded_page_kristina.html'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title of the page
page_title = soup.title.string if soup.title else "No title found"
print("Page Title:", page_title)

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
        headers = []
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


print(type(all_table_data))
print(all_table_data)

print(type(all_data))
print(all_data)
# Flatten the list of lists
flattened_data = [item for sublist in all_data for item in sublist]

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(flattened_data)

# Save DataFrame to CSV
df.to_csv('parsed.csv', index=False)


# Print all table data
for index, (headers, table_data) in enumerate(all_table_data):
    print(f"\nTable {index + 1}:")
    print(headers)
    for row in table_data:
        print(row)

# Save each table in a separate CSV file
for index, (headers, table_data) in enumerate(all_table_data):
    csv_file_path = f'table_{index + 1}.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(table_data)
    print(f"Table {index + 1} saved to {csv_file_path}")
