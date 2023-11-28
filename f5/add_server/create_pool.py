from f5.bigip import ManagementRoot

# F5 Device Connection Details
f5_host = 'f5_host_ip_or_name'
f5_username = 'username'
f5_password = 'password'

# Connect to F5
mgmt_root = ManagementRoot(f5_host, f5_username, f5_password)

# Node Details
node_name = 'new_node_name'
node_ip = 'server_ip_address'

# Pool Details
pool_name = 'new_pool_name'

# Create Pool
new_pool = mgmt_root.tm.ltm.pools.pool.create(name=pool_name)

# Add Node to Pool
pool_member = new_pool.members_s.members.create(name=f"{node_name}:port")
# Replace 'port' with the actual port number
