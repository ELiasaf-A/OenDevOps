from f5.bigip import ManagementRoot

# Replace with your F5 host, username, and password
host = 'your_host'
username = 'your_username'
password = 'your_password'

try:
    # Connect to the F5 device
    mgmt = ManagementRoot(f5_host, username, password)

    # Access the LTM component
    ltm = mgmt.tm.ltm

    # Fetch the specific policy
    policy_name = 'Comax_DLL'  # Replace with your policy name
    policy = ltm.policys.policy.load(name=policy_name)
    rules = policy.rules_s.get_collection()

    # Extract and print details of each rule
    for rule in rules:
        print(f"Rule Name: {rule.name}")
        conditions = rule.conditions_s.get_collection()
        actions = rule.actions_s.get_collection()

        # Print conditions
        for cond in conditions:
            print(f"  Condition - {cond.name}: {cond.raw}")

        # Print actions
        for act in actions:
            print(f"  Action - {act.name}: {act.raw}")

        print("-------------")

except Exception as e:
    print(f"Error: {e}")
