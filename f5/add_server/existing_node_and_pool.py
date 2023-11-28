# Pool and Node Details
pool_name = 'existing_pool_name'  # Name of the pool to add the node to
node_name = 'existing_node_name'  # Name of the existing node
node_port = 80  # Port number the node is listening on, change as needed

# Reference the existing pool
pool = mgmt_root.tm.ltm.pools.pool.load(name=pool_name)

# Reference the existing node
# No need to load the node separately if you are just adding it to the pool




# Add the existing node to the pool
member = pool.members_s.members.create(name=f"{node_name}:{node_port}")



