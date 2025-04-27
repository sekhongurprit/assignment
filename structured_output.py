import os
import json
import pandas as pd

# Define the folder where JSON files are stored
output_folder = 'out/'

# Fields that can be searched
fields_of_interest = ['Patient Name', 'Doctor Name', 'Date', 'Medications', 'Special Instructions']

# Load all JSON files and collect their content
data = []

for filename in os.listdir(output_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(output_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                content = json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding {filename}")
                continue
        
        record = {'File': filename}
        for field in fields_of_interest:
            record[field] = content.get(field, None)
        
        data.append(record)

# Convert into a DataFrame for easier querying
df = pd.DataFrame(data)

# Print available fields
print("Available fields to search:", fields_of_interest)

# Ask the user for the search field
search_field = input("Enter the field you want to search (e.g., 'Patient Name'): ").strip()

if search_field not in fields_of_interest:
    print(f"Invalid field name. Please choose from: {fields_of_interest}")
    exit()

# Ask the user for the search value
search_value = input(f"Enter the value to search for in '{search_field}': ").strip()

# Search: case-insensitive, ignoring NaN values
matches = df[df[search_field].str.contains(search_value, case=False, na=False)]

# Print the results
if not matches.empty:
    print(f"\nFound {len(matches)} matching records:\n")
    for index, row in matches.iterrows():
        print(f"File: {row['File']}")
        for field in fields_of_interest:
            print(f"{field}: {row[field]}")
        print("-" * 50)
else:
    print("\nNo matching records found.")

