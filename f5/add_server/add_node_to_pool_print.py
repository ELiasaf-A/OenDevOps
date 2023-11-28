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
node_port = 80  # Replace with the actual port number your node is listening on

# Specify the partition
partition = 'Common'  # Replace with your actual partition name

# Reference the existing pool
try:
    pool = mgmt_root.tm.ltm.pools.pool.load(name=pool_name, partition=partition)
except Exception as e:
    print(f"Error loading pool: {e}")
    exit(1)

# Add the existing node to the pool
try:
    member = pool.members_s.members.create(name=f"{node_name}:{node_port}", partition=partition)
except Exception as e:
    print(f"Error adding member to pool: {e}")
