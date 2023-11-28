from f5.bigip import ManagementRoot
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def connect_to_f5(host, username, password):
    """
    Connect to F5 BIG-IP device.
    """
    try:
        return ManagementRoot(host, username, password)
    except Exception as e:
        logger.error(f"Error connecting to F5: {e}")
        return None


def modify_or_load_policy(f5_conn, policy_name, strategy):
    """
    Modify an existing policy or load it if it exists.
    """
    try:
        return f5_conn.tm.ltm.policys.policy.load(name=policy_name, partition='Common')
    except Exception as e:
        logger.error(f"Policy not found, attempting to create a new one: {e}")
        try:
            return f5_conn.tm.ltm.policys.policy.create(
                name=policy_name,
                partition='Common',
                subPath='Drafts',
                strategy=strategy
            )
        except Exception as e:
            logger.error(f"Error creating policy: {e}")
            return None


def add_rule_to_policy(policy, rule_name):
    """
    Add a rule to the specified policy.
    """
    try:
        return policy.rules_s.rules.create(name=rule_name)
    except Exception as e:
        logger.error(f"Error adding rule: {e}")
        return None


def add_condition_to_rule(rule, condition_name, path_value):
    """
    Add a condition to a rule.
    """
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
        logger.error(f"Error adding condition: {e}")


def add_action_to_rule(rule, action_name, pool_name):
    """
    Add an action to a rule.
    """
    try:
        rule.actions_s.actions.create(
            name=action_name,
            pool=pool_name,
            forward=True
        )
    except Exception as e:
        logger.error(f"Error adding action: {e}")


def add_rules_to_policy(f5_conn, policy_name, pools_file, base_path, strategy):
    """
    Add rules to the specified policy based on the pool names.
    """
    policy = modify_or_load_policy(f5_conn, policy_name, strategy)
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
        logger.info(f"Added rules to policy '{policy_name}' successfully")


def main():
    """
    Main function to execute the script.
    """
    host = 'your_host'
    username = 'your_username'
    password = 'your_password'
    f5_connection = connect_to_f5(host, username, password)
    if f5_connection:
        pools_file_path = ('/pool-name-server')  # Update with
        # your file path
        policy_name = 'policy_name'
        base_path = '/max2000/complusadmin/iis'
        strategy = '/Common/first-match'

        if os.path.exists(pools_file_path):
            add_rules_to_policy(f5_connection, policy_name, pools_file_path, base_path, strategy)
        else:
            logger.error(f"Pools file not found at {pools_file_path}")


if __name__ == '__main__':
    main()
