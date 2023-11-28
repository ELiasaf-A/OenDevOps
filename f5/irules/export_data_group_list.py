import csv
from f5.bigip import ManagementRoot

# F5 BigIP Connection Details
host = 'your_host'
username = 'your_username'
password = 'your_password'

# Connect to the BigIP
mgmt = ManagementRoot(host, username, password)

# Data Group List name (adjust for correct partition if necessary)
data_group_name = 'name data group'

# Retrieve Data Group List
data_group = mgmt.tm.ltm.data_group.internals.internal.load(name=data_group_name)

# Extract information - focusing on string records
data_group_records = [{
    'name': record['name'],
    'data': record['data']
} for record in data_group.records]

# Write to CSV
with open('data_group_records.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing the headers
    writer.writerow(['Name', 'Data'])
    # Writing the data
    for record in data_group_records:
        writer.writerow([record['name'], record['data']])

print("Data Group List records exported to data_group_records.csv")
