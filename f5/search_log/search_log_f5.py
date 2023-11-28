import re
import csv

# Define the path to your log file
log_file_path = '/Users/eliasafabargel/Library/Mobile Documents/com~apple~CloudDocs/DevSecOps/f5/search_log/Logs.txt'


# Regex patterns to capture the needed information
request_pattern = re.compile(r'Client (\d+\.\d+\.\d+\.\d+):\d+ -> (ws\.comax\.co\.il/[\S]+) \((request)\)')
content_type_pattern = re.compile(r'Content-Type: ([^;]+; charset=utf-8; action="([^"]+)")')
soap_action_pattern = re.compile(r'SOAPAction: "([^"]+)"')

# Set to store unique combinations of IP, Content-Type, and SOAPAction
unique_entries = set()

# List to store the extracted data
data_list = []

# Open the log file and process each line
with open(log_file_path, 'r') as log_file:
    current_data = {}
    for line in log_file:
        # Check if we are at the start of a new request
        request_match = request_pattern.search(line)
        if request_match:
            # If we have collected data for a previous request, let's check if it's complete and unique
            if current_data and 'Content-Type' in current_data and 'SOAPAction' in current_data:
                unique_key = (current_data['Client IP'], current_data['Content-Type'], current_data['SOAPAction'])
                if unique_key not in unique_entries:
                    unique_entries.add(unique_key)
                    data_list.append(current_data)

            # Start a new block of data collection
            current_data = {
                'Client IP': request_match.group(1),
                'URL': request_match.group(2),
                'Content-Type': None,
                'SOAPAction': None
            }

        # If we are within a request block, collect Content-Type and SOAPAction
        elif current_data:
            content_type_match = content_type_pattern.search(line)
            soap_action_match = soap_action_pattern.search(line)

            if content_type_match:
                current_data['Content-Type'] = content_type_match.group(1)
            if soap_action_match:
                current_data['SOAPAction'] = soap_action_match.group(1)

    # Check for the last entry after the loop ends
    if current_data and 'Content-Type' in current_data and 'SOAPAction' in current_data:
        unique_key = (current_data['Client IP'], current_data['Content-Type'], current_data['SOAPAction'])
        if unique_key not in unique_entries:
            unique_entries.add(unique_key)
            data_list.append(current_data)

# Write the extracted data to a CSV file
csv_file_path = 'extracted_data.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['Client IP', 'URL', 'Content-Type', 'SOAPAction']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()  # Write the header
    for data in data_list:
        writer.writerow(data)

print(f"Data has been extracted and saved to {csv_file_path}")
