from f5.bigip import ManagementRoot
import csv


def connect_to_f5(host, username, password):
    try:
        f5 = ManagementRoot(host, username, password)
        return f5
    except Exception as e:
        print(f"Error connecting to F5: {e}")
        return None


def get_policies(f5_connection):
    try:
        return f5_connection.tm.ltm.policys.get_collection()
    except Exception as e:
        print(f"Error retrieving policies: {e}")
        return []


def get_policy_settings(policy):
    settings = []
    for rule in policy.rules_s.get_collection():
        settings.append(rule.name)
    return ', '.join(settings)


def export_policies_to_csv(policies, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Policy Name', 'Partition', 'Settings'])
        for policy in policies:
            settings = get_policy_settings(policy)
            writer.writerow([policy.name, policy.partition, settings])


f5_connection = connect_to_f5('your-f5-host', 'your-username', 'your-password')
if f5_connection:
    policies = get_policies(f5_connection)
    export_policies_to_csv(policies, 'f5_policies.csv')
    print("Policies exported to f5_policies.csv")
