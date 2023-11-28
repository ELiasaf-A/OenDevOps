import os
import paramiko

def create_sftp_client(host, port, username, password):
    """
    Creates an SFTP client connected to the specified host on the specified port.
    """
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, username, password)
    return client.open_sftp()

def move_files_sftp(sftp, start_path, dest_path, pattern):
    for filename in os.listdir(start_path):
        if pattern in filename:
            local_path = os.path.join(start_path, filename)
            remote_path = os.path.join(dest_path, filename)
            sftp.put(local_path, remote_path)
            os.remove(local_path)

# SFTP Connection Details
host = 'your_sftp_server_address'
port = 22  # default SFTP port
username = 'your_username'
password = 'your_password'

# SFTP Paths (adjust as necessary)
remote_path_items = '/remote/path/for/items'
remote_path_inbound = '/remote/path/for/inbound'
remote_path_shipments = '/remote/path/for/shipments'

# Local Paths (adjust as necessary)
local_path = 'S:\\StoreDirect\\1589\\01\\out\\'

# Establish SFTP Connection
sftp = create_sftp_client(host, port, username, password)

# Transfer Files
move_files_sftp(sftp, local_path, remote_path_items, 'ITEMS')
move_files_sftp(sftp, local_path, remote_path_inbound, 'Inbound')
move_files_sftp(sftp, local_path, remote_path_shipments, '\\d')  # regex for files starting with numbers

# Close SFTP Connection
sftp.close()

print("SFTP file transfer complete.")
