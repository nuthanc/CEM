import os
import yaml
from subprocess import check_output
import time


TEST_INPUT = 'test_input.yaml'


def get_nodes():
    with open(TEST_INPUT) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    for k, v in data['instances'].items():
        print(v['ip'])
    return list(data['instances'].keys())


def wait_for_nodes_to_deploy(nodes):
    for node in nodes:
        status = check_output(
            f"juju status|grep {node}", shell=True, universal_newlines=True).strip()
        print(status)
        while 'Deployed' not in status:
            time.sleep(5)
            status = check_output(
                f"juju status|grep {node}", shell=True, universal_newlines=True).strip()
            print(status)


def update_etc_hosts():
    os.system('python3 etc-hosts.py')


def update_host_templates():
    os.system('python3 etc-hosts-in-template.py')


def main():
    nodes = get_nodes()
    wait_for_nodes_to_deploy(nodes)
    update_etc_hosts()
    update_host_templates()


if __name__ == '__main__':
    main()
    # nodes = get_nodes()
    # wait_for_nodes_to_deploy(nodes)
    # update_etc_hosts()
    # update_host_templates()
