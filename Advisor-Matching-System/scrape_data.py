import requests
from bs4 import BeautifulSoup
import openpyxl
import re

# Make a request to the website
response = requests.get('https://cs.illinois.edu/about/people/all-faculty')

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create an Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'CS Faculty'

    # Initialize row counter
    row_name = 1
    row_title = 3  # Start from the third row for titles
    row = 3  # Start from the third row for photo URLs

    # Get the names and titles from the website
    for name_div in soup.select('div[class*="name"]'):
        # Extract and clean up the name text
        name_text = name_div.get_text(strip=True)
        # Write the name to the first column (A) of the current row
        sheet[f'A{row_name}'] = name_text
        row_name += 1

    for title_div in soup.select('div[class*="title"]'):
        # Extract and clean up the title text
        title_text = title_div.get_text(strip=True)
        # Write the title to the second column (B) of the current row
        sheet[f'B{row_title}'] = title_text
        row_title += 1
    
    for person_div in soup.select('div.item.person'):
        # Extract photo URL
        photo_div = person_div.find('div', class_='photo')
        photo_style = photo_div.get('style', '')
        photo_url_match = re.search(r'url\((.*?)\)', photo_style)
        photo_url = photo_url_match.group(1) if photo_url_match else 'No photo available'

        # Extract href from name div
        name_div = person_div.find('div', class_='name')
        href = name_div.find('a')['href'] if name_div and name_div.find('a') else 'No link available'

        # Write data to the sheet
        sheet[f'C{row}'] = 'https:'+photo_url
        sheet[f'D{row}'] = 'https://cs.illinois.edu' + href
        row += 1

    # Save the workbook
    excel_file_path = 'uiuc_cs_faculty.xlsx'
    workbook.save(excel_file_path)
    print(f"Faculty names and titles have been saved to '{excel_file_path}'")
else:
    print(f"Failed to retrieve the webpage: Status code {response.status_code}")
