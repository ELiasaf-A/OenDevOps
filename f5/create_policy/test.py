from f5.bigip import ManagementRoot

def connect_to_f5(host, username, password):
    try:
        f5 = ManagementRoot(host, username, password)
        return f5
    except Exception as e:
        print(f"Error connecting to F5: {e}")
        return None

def create_policy(f5_conn, policy_name, strategy):
    try:
        policy = f5_conn.tm.ltm.policys.policy.create(
            name=policy_name,
            partition='Common',
            subPath='Drafts',  # Typically, policies are created in Drafts
            strategy=strategy
        )
        return policy
    except Exception as e:
        print(f"Error creating policy: {e}")
        return None

def add_rule_to_policy(policy, rule_name):
    try:
        rule = policy.rules_s.rules.create(name=rule_name)
        return rule
    except Exception as e:
        print(f"Error adding rule: {e}")
        return None

def add_condition_to_rule(rule, condition_name, path_value):
    try:
        rule.conditions_s.conditions.create(
            name=condition_name,
            httpUri=True,
            path=True,
            values=[path_value],
            caseInsensitive=True,
            equals=True,
            external=True,
            index=0,
            present=True,
            remote=True,
            request=True
        )
    except Exception as e:
        print(f"Error adding condition: {e}")

def add_action_to_rule(rule, action_name, pool_name):
    try:
        rule.actions_s.actions.create(
            name=action_name,
            pool=pool_name,
            forward=True
        )
    except Exception as e:
        print(f"Error adding action: {e}")

def main():
    f5_connection = connect_to_f5('your-f5-host', 'your-username', 'your-password')
    if f5_connection:
        # Create a new policy
        new_policy = create_policy(f5_connection, 'Comax-Dll-Opr', '/Common/first-match')
        if new_policy:
            # Add a rule to the new policy
            new_rule = add_rule_to_policy(new_policy, 'ComPlusAdmin-opr01')
            if new_rule:
                # Add condition and action to the rule
                add_condition_to_rule(new_rule, '0', '/max2000/complusadmin/comax-opr01.asp')
                add_action_to_rule(new_rule, '0', '/Common/Pool-comax-opr01')
                print("Policy and rule created successfully")

if __name__ == '__main__':
    main()
