import os
import ftplib

def create_ftp_client(host, username, password):
    """
    Creates an FTP client connected to the specified host with the given credentials.
    """
    ftp = ftplib.FTP(host)
    ftp.login(username, password)
    return ftp

def move_files_ftp_upload(ftp, start_path, dest_path, pattern):
    for filename in os.listdir(start_path):
        if pattern in filename:
            local_path = os.path.join(start_path, filename)
            remote_path = os.path.join(dest_path, filename)
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
            os.remove(local_path)

def move_files_ftp_download(ftp, start_path, dest_path, pattern):
    ftp.cwd(start_path)
    for filename in ftp.nlst():
        if pattern in filename:
            local_path = os.path.join(dest_path, filename)
            remote_path = os.path.join(start_path, filename)
            with open(local_path, 'wb') as file:
                ftp.retrbinary(f'RETR {remote_path}', file.write)
            ftp.delete(remote_path)

# FTP Connection Details
host = 'ip '  # Use your actual FTP server address
username = 'user'      # Use your actual FTP username
password = 'passs'  # Use your actual FTP password

# FTP Remote Paths (adjust as necessary)
remote_path_items = '/TOMAHLEV/PART'
remote_path_inbound = '/TOMAHLEV/POs'
remote_path_shipments = '/TOMAHLEV/LOADED'
remote_download_path = '/TOMASL'

# Local Paths (adjust as necessary)
local_upload_path = 'S:\\StoreDirect\\1589\\01\\out\\'
local_download_path = 'S:\\StoreDirect\\1589\\01\\in\\'

# Establish FTP Connection
ftp = create_ftp_client(host, username, password)

# Upload Files
move_files_ftp_upload(ftp, local_upload_path, remote_path_items, 'ITEMS')
move_files_ftp_upload(ftp, local_upload_path, remote_path_inbound, 'Inbound')
move_files_ftp_upload(ftp, local_upload_path, remote_path_shipments, '\\d')  # regex for files starting with numbers

# Download Files
move_files_ftp_download(ftp, remote_download_path, local_download_path, '')  # Download all files from remote_download_path

# Close FTP Connection
ftp.quit()

print("FTP file transfer complete.")
