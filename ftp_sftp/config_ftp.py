import os
import shutil
import re

def move_files(start_path, dest_path, pattern):
    for filename in os.listdir(start_path):
        if re.match(pattern, filename):
            shutil.move(os.path.join(start_path, filename), os.path.join(dest_path, filename))

# Paths
source_path = 'S:\\StoreDirect\\1589\\01\\out\\'
client_path_items = 'D:\\priority\\system\\load\\MASLEMNEW\\TOMAHLEV\\PART'
client_path_inbound = 'D:\\priority\\system\\load\\MASLEMANY\\TOMAHLEV\\POs'
client_path_shipments = 'D:\\priority\\system\\load\\MASLEMANY\\TOMAHLEV\\SHIPMENTS'
client_old_path = 'D:\\priority\\system\\load\\MASLEMNEW\\TOMASL'
destination_path = 'S:\\StoreDirect\\1589\\01\\in'

# Moving files
move_files(source_path, client_path_items, r'^ITEMS')
move_files(source_path, client_path_inbound, r'^Inbound')
move_files(source_path, client_path_shipments, r'^\d')  # Files starting with numbers
move_files(client_old_path, destination_path, r'.*')  # Move all files

print("File transfer complete.")
