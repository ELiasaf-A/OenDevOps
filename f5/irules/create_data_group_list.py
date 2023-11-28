import csv
from f5.bigip import ManagementRoot

# F5 BigIP Connection Details
host = 'your_host'
username = 'your_username'
password = 'your_password'

# Connect to the BigIP
mgmt = ManagementRoot(host, username, password)

# New Data Group List name
new_data_group_name = 'name_data_group'

# Read data from CSV
records = []
with open('data_group_records.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        records.append({'name': row['Name'], 'data': row['Data']})

# Create a new Data Group List
new_data_group = mgmt.tm.ltm.data_group.internals.internal.create(
    name=new_data_group_name, type='string', records=records
)

print(f"New Data Group List '{new_data_group_name}' created with records from the CSV file.")
