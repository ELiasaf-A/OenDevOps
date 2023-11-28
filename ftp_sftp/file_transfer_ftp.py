import os
import ftplib

def create_ftp_client(host, username, password):
    """
    Creates an FTP client connected to the specified host with the given credentials.
    """
    ftp = ftplib.FTP(host)
    ftp.login(username, password)
    return ftp

def move_files_ftp(ftp, start_path, dest_path, pattern):
    for filename in os.listdir(start_path):
        if pattern in filename:
            local_path = os.path.join(start_path, filename)
            remote_path = os.path.join(dest_path, filename)
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
            os.remove(local_path)

# FTP Connection Details
host = 'your_ftp_server_address'
username = 'your_username'
password = 'your_password'

# FTP Paths (adjust as necessary)
remote_path_items = '/remote/path/for/items'
remote_path_inbound = '/remote/path/for/inbound'
remote_path_shipments = '/remote/path/for/shipments'

# Local Paths (adjust as necessary)
local_path = 'S:\\StoreDirect\\1589\\01\\out\\'

# Establish FTP Connection
ftp = create_ftp_client(host, username, password)

# Transfer Files
move_files_ftp(ftp, local_path, remote_path_items, 'ITEMS')
move_files_ftp(ftp, local_path, remote_path_inbound, 'Inbound')
move_files_ftp(ftp, local_path, remote_path_shipments, '\\d')  # regex for files starting with numbers

# Close FTP Connection
ftp.quit()

print("FTP file transfer complete.")
