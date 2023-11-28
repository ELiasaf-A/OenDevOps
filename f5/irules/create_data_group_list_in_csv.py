import csv
import logging
from f5.bigip import ManagementRoot

# Logging configuration
logging.basicConfig(level=logging.INFO)

def create_data_group(mgmt, data_group_name, csv_file):
    try:
        records = []
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append({'name': row['Name'], 'data': row['Data']})

        new_data_group = mgmt.tm.ltm.data_group.internals.internal.create(
            name=data_group_name, type='string', records=records
        )
        logging.info(f"New Data Group List '{data_group_name}' created with records from the CSV file.")
    except Exception as e:
        logging.error(f"Error creating data group: {e}")

# Connection parameters (consider fetching these securely from environment variables or a config file)
host = 'your_host'
username = 'your_username'
password = 'your_password'
data_group_name = 'name_data_group'
csv_file_path = 'data_group_records.csv'

# Connect to the BigIP
try:
    mgmt = ManagementRoot(host, username, password)
    create_data_group(mgmt, data_group_name, csv_file_path)
except Exception as e:
    logging.error(f"Connection or operation failed: {e}")
