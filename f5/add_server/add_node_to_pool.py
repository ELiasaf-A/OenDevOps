from f5.bigip import ManagementRoot

# F5 Device Connection Details
f5_host = 'f5_host_ip_or_name'
f5_username = 'username'
f5_password = 'password'

# Connect to F5
mgmt_root = ManagementRoot(f5_host, f5_username, f5_password)

# Pool and Node Details
pool_name = 'existing_pool_name'
node_name = 'existing_node_name'
node_port = 80  # Change as needed
partition = 'Common'  # Replace with your partition name if different

# Reference the existing pool
pool = mgmt_root.tm.ltm.pools.pool.load(name=pool_name, partition=partition)

# Add the existing node to the pool
member = pool.members_s.members.create(name=f"{node_name}:{node_port}", partition=partition)
