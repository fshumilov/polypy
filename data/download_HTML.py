# The main goal to download the HTML code of
# a database web page as a HTML file to parcing needs

# main source: https://www.campusplastics.com/
# e.g. https://www.campusplastics.com/campus/en/datasheet/Ultraform%C2%AE+N2640+Z2+Q600/BASF/20/b0d878b6/SI?pos=4
# target material: Polyurethane

import requests

url = 'https://www.campusplastics.com/campus/en/datasheet/Ultraform%C2%AE+N2640+Z2+Q600/BASF/20/b0d878b6/SI?pos=4'

# Define headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Open a file in write mode with UTF-8 encoding
    with open('downloaded_page.html', 'w', encoding='utf-8') as file:
        # Write the HTML content to the file
        file.write(response.text)
    print("HTML page downloaded successfully!")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
