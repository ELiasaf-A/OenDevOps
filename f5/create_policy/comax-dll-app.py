from f5.bigip import ManagementRoot


def connect_to_f5(host, username, password):
    try:
        f5 = ManagementRoot(host, username, password)
        return f5
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


def add_rules_to_policy(f5_conn, policy_name, num_rules, base_path, base_pool, strategy):
    policy = create_or_load_policy(f5_conn, policy_name, strategy)
    if policy:
        for i in range(1, num_rules + 1):
            rule_name = f"ComPlusAdmin-app{i:02d}"
            path_value = f"{base_path}{i:02d}.asp"
            pool_name = f"/Common/{base_pool}{i:02d}"
            rule = add_rule_to_policy(policy, rule_name)
            if rule:
                add_condition_to_rule(rule, '0', path_value)
                add_action_to_rule(rule, '0', pool_name)

        policy.update()
        print(f"Added {num_rules} rules to policy '{policy_name}' successfully")


def main():
    f5_connection = connect_to_f5('your-f5-host', 'your-username', 'your-password')
    if f5_connection:
        add_rules_to_policy(
            f5_connection,
            'Policy_name_Change',
            20,
            '/max2000/complusadmin/name-pool',
            'Pool-name-server',
            '/Common/first-match'
        )


if __name__ == '__main__':
    main()
