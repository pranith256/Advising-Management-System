import openpyxl
import json

def update_json_with_excel(json_file_path, excel_file_path, output_json_file_path):
    # Load the JSON data
    with open(json_file_path, 'r') as file:
        professors_data = json.load(file)

    # Load the Excel data
    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook.active

    # Iterate over the rows in the Excel sheet, starting from the third row
    for row in sheet.iter_rows(min_row=3):
        # Extract professor name, photo URL, and profile URL
        professor_name = row[0].value.strip()  if row[0].value else None
        if professor_name and professor_name in professors_data:
            # Check and extract photo URL and profile URL if they exist
            photo_url = row[2].value.strip() if row[2].value else None
            profile_url = row[3].value.strip() if row[3].value else None

            # Update the professor's data in the JSON file
            professors_data[professor_name]['photo'] = photo_url if photo_url else "Not Available"
            professors_data[professor_name]['url'] = profile_url if profile_url else "Not Available"


    # Save the updated JSON data
    with open(output_json_file_path, 'w') as file:
        json.dump(professors_data, file, indent=4)

json_file_path = 'FinalProfessorsData.json'
excel_file_path = 'faculty.xlsx'
output_json_file_path = '2UpdatedFinalProfessorsData.json'

update_json_with_excel(json_file_path, excel_file_path, output_json_file_path)
