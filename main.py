import pdfplumber
import csv

pdf_path = 'NationalShippersContactList.pdf'
csv_file_path = 'growers_list_split.csv'


def process_row(row):
    try:
        # first part of the string up to the first comma is the name
        parts = row[0].split(',')  # Split the string by commas
        if len(parts) >= 3:
            # If there are at least three parts, the second part is city, and the third part is state
            name_part = parts[0]
            city = parts[1]
            state = parts[2]
        elif len(parts) == 2:
            # Handle cases with only one comma; assume city and state are combined or only one is present
            name_part = parts[0]
            city = parts[1]
            state = ''  # Use an empty string or a placeholder if no separate state info
        else:
            # Fallback for unexpected format; could log these cases for review
            name_part = row[0]
            city = ''
            state = ''
    except ValueError:
        # Fallback in case of unexpected errors
        name_part = row[0]
        city = ''
        state = ''

    # Trim whitespace and return the updated row with name, city, and state as separate elements
    return [name_part.strip()] + [city.strip()] + [state.strip()] + row[1:]


# Note: Ensure this function is called appropriately when iterating through each row of the table data


# Open the PDF and CSV files
with pdfplumber.open(pdf_path) as pdf, open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'City', 'State', 'Phone', 'Email'])  # Adjust headers based on actual data columns

    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table[1:]:  # Skip the header row of the table if present
                processed_row = process_row(row)
                writer.writerow(processed_row)

print("Data extracted and written to 'growers_list_split.csv' successfully!")
