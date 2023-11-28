from f5.bigip import ManagementRoot


def connect_to_f5(host, username, password):
    try:
        return ManagementRoot(host, username, password)
    except Exception as e:
        print(f"Error connecting to F5: {e}")
        return None


def create_or_load_policy(f5_conn, policy_name, strategy):
    try:
        try:
            return f5_conn.tm.ltm.policys.policy.load(name=policy_name, partition='Common')
        except Exception:
            return f5_conn.tm.ltm.policys.policy.create(
                name=policy_name,
                partition='Common',
                subPath='Drafts',
                strategy=strategy
            )
    except Exception as e:
        print(f"Error creating/loading policy: {e}")
        return None


def add_rule_to_policy(policy, rule_name):
    try:
        return policy.rules_s.rules.create(name=rule_name)
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


def add_rules_to_policy(f5_conn, policy_name, pools_file, base_path, strategy):
    policy = create_or_load_policy(f5_conn, policy_name, strategy)
    if policy:
        with open(pools_file, 'r') as file:
            for pool_name in file:
                pool_name = pool_name.strip()
                rule_number = pool_name[-2:]  # Extract the number from pool name
                rule_name = f"ComPlusAdmin-{rule_number}"
                path_value = f"{base_path}{rule_number}.asp"
                rule = add_rule_to_policy(policy, rule_name)
                if rule:
                    add_condition_to_rule(rule, '0', path_value)
                    add_action_to_rule(rule, '0', f"/Common/{pool_name}")

        policy.update()
        print(f"Added rules to policy '{policy_name}' successfully")


def main():
    f5_connection = connect_to_f5('your-f5-host', 'your-username', 'your-password')
    if f5_connection:
        pools_file = ('/Users/eliasafabargel/Library/Mobile '
                      'Documents/com~apple~CloudDocs/DevSecOps/f5/pools_server/pool-name-server.txt')  # Update with the
        # path to your file
        add_rules_to_policy(
            f5_connection,
            'Comax-Dll-IIS',
            pools_file,
            '/max2000/complusadmin/iis',  # Base path for conditions
            '/Common/first-match'  # Strategy for the policy
        )


if __name__ == '__main__':
    main()
