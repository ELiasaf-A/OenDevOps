import csv
from f5.bigip import ManagementRoot

# F5 Device Connection Details
f5_host = 'f5_host_ip_or_name'
f5_username = 'username'
f5_password = 'password'

# Connect to F5
mgmt_root = ManagementRoot(f5_host, f5_username, f5_password)

# Read servers from CSV file
csv_file = '../pools_server/naew_server_dr.csv'

with open(csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader.fieldnames)  # This line will print the column names
    for row in reader:
        server_name = row['name']
        server_ip = row['ip']

        # Node Details
        node_name = f"dr-{server_name}"
        node_port = 80  # Replace with the actual port number your node is listening on

        # Create Node
        new_node = mgmt_root.tm.ltm.nodes.node.create(
            name=node_name,
            address=server_ip,
            partition='Common',
            description= f"dr-{server_name}"  # Add your desired description
        )

        # Pool Details
        pool_name = f"Pool-{node_name}"

        # Create Pool
        new_pool = mgmt_root.tm.ltm.pools.pool.create(
            name=pool_name,
            monitor='gateway_icmp',  # Set health monitor
            partition='Common',
            description= f"dr-{server_name}"  # Add your desired description
        )

        # Add Node to Pool
        pool_member = new_pool.members_s.members.create(
            name=f"{node_name}:{node_port}",
            partition='Common',
            description= f"dr-{server_name}"  # Add your desired description
        )
