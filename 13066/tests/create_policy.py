from ruamel.yaml import YAML
import pprint

def construct_config_map(policies=None):
    policy_dict = {}
    policy_dict['apiVersion'] = 'v1'
    policy_dict['kind'] = 'ConfigMap'
    policy_dict['metadata'] = {
        'name': 'k8s-auth-policy',
        'namespace': 'kube-system',
        'labels': {
            'k8s-app': 'k8s-keystone-auth'
        }
    }
    if policies is None:
        policies = [
            {
                'resource': {
                    'verbs': ['*'],
                    'resources': ['*'],
                    'version': '*',
                    'namespace': '*'
                },
                'match': [
                    {
                        'type': 'role',
                        'values': ['*']
                    },
                    {
                        'type': 'project',
                        'values': ['admin']
                    }
                ]
            }
        ]

    policy_dict['data'] = {
        'policies': policies
    }
    return policy_dict


def create_config_map_file(policy_dict, filename=None):
    if filename is None:
        filename = 'auth_policy.yaml'
    yaml = YAML()
    yaml.dump(policy_dict, open(filename, 'w'))


def create_policies(resource={}, match=[]):
    if resource.get('verbs') is None:
        resource['verbs'] = ['*']
    if resource.get('resources') is None:
        resource['resources'] = ['*']
    if resource.get('version') is None:
        resource['version'] = ['*']
    if resource.get('namespace') is None:
        resource['namespace'] = ['*']

    if len(match) == 0:
        role_dict = {
            'type': 'role',
            'values': ['*']
        }
        project_dict = {
            'type': 'project',
            'values': ['admin']
        }
        match.append(role_dict)
        match.append(project_dict)

    policies = [{'resource': resource, 'match': match}]
    return policies


# pprint.pprint(create_policies(resource={'verbs': ['get'], 'resources': ['Pod']}))
# policies = create_policies(resource={'verbs': ['get'], 'resources': ['Pod']})
# policy_dict = construct_config_map(policies)
# create_config_map_file(policy_dict)
