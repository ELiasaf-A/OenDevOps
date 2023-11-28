import csv
from f5.bigip import ManagementRoot

# F5 BIG-IP Connection Parameters
host = 'your_host'
username = 'your_username'
password = 'your_password'

# Connect to the BIG-IP
mgmt = ManagementRoot(hostname, username, password)

# Fetch the list of pools
pools = mgmt.tm.ltm.pools.get_collection()

# Prepare data for CSV
data = []

for pool in pools:
    pool_name = pool.name
    pool_members = pool.members_s.get_collection()

    for member in pool_members:
        node = {
            'pool_name': pool_name,
            'node_name': member.name,
            'status': member.state
        }
        data.append(node)

# Write data to CSV
with open('f5_pools_and_nodes.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['pool_name', 'node_name', 'status'])
    writer.writeheader()
    writer.writerows(data)

print("Data has been written to f5_pools_and_nodes.csv")
