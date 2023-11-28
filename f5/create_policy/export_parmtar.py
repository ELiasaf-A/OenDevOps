from f5.bigip import ManagementRoot
import csv

# Replace these with your actual F5 host, username, and password
host = 'your_host'
username = 'your_username'
password = 'your_password'

try:
    # Connect to the F5 device
    mgmt = ManagementRoot(f5_host, username, password)

    # Access the LTM (Local Traffic Manager) component
    ltm = mgmt.tm.ltm

    # Fetch the specific policy
    policy = ltm.policys.policy.load(name='comaxerp_redirect')
    rules = policy.rules_s.get_collection()

    # Extracting detailed policy and rules settings
    policy_data = []
    for rule in rules:
        # Fetching conditions and actions for each rule
        conditions = rule.conditions_s.get_collection()
        actions = rule.actions_s.get_collection()

        # Process conditions
        condition_details = [f"{cond.name}: {cond.raw}" for cond in conditions]

        # Process actions
        action_details = [f"{act.name}: {act.raw}" for act in actions]

        # Rule details
        rule_details = {
            'Rule Name': rule.name,
            'Conditions': ', '.join(condition_details),
            'Actions': ', '.join(action_details)
        }
        policy_data.append(rule_details)

    # Write policy data to a CSV file
    with open('policy_details.csv', 'w', newline='') as csvfile:
        fieldnames = ['Rule Name', 'Conditions', 'Actions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in policy_data:
            writer.writerow(data)

    print("Detailed policy and rules settings exported to policy_details.csv")

except Exception as e:
    print(f"Error: {e}")
