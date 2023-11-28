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

# Create Node
new_node = mgmt_root.tm.ltm.nodes.node.create(name=node_name, address=node_ip)
