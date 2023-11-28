import csv
from f5.bigip import ManagementRoot

# F5 BigIP Connection Details
host = 'your_host'
username = 'your_username'
password = 'your_password'

# Connect to the BigIP
mgmt = ManagementRoot(host, username, password)

# iRule name to retrieve
irule_name = 'your_irule_name'

# Retrieve iRule
irule = mgmt.tm.ltm.rules.rule.load(name=irule_name)

# Extract information
irule_info = {
    'name': irule.name,
    'definition': irule.apiAnonymous
}

# Write to CSV
with open('irule_info.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing the headers
    writer.writerow(irule_info.keys())
    # Writing the data
    writer.writerow(irule_info.values())

print("iRule information exported to irule_info.csv")
