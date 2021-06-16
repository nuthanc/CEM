import os
import yaml
from subprocess import check_output
import time
from jinja2 import Environment, FileSystemLoader


TEST_INPUT = 'test_input.yaml'


def get_nodes():
    with open(TEST_INPUT) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return list(data['instances'].keys())


def wait_for_nodes_to_deploy(nodes):
    for node in nodes:
        status = check_output(
            f"juju status|grep {node}", shell=True, universal_newlines=True).strip()
        print(status, flush=True)
        while 'Deployed' not in status:
            time.sleep(5)
            status = check_output(
                f"juju status|grep {node}", shell=True, universal_newlines=True).strip()
            print(status, flush=True)


def update_etc_hosts():
    os.system('python3 etc-hosts.py')


def update_host_templates():
    os.system('python3 etc-hosts-in-template.py')

def update_test_input():
    auth_ip = check_output("juju status|grep 5000|awk '{print $5}'", shell=True, universal_newlines=True).strip()
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
    env = Environment(loader=FileSystemLoader(THIS_DIR))
    template = env.get_template(f"{TEST_INPUT}.j2")
    with open(TEST_INPUT, 'w') as f:
        f.write(template.render(auth_ip=auth_ip))

def main():
    nodes = get_nodes()
    wait_for_nodes_to_deploy(nodes)
    update_test_input()
    update_etc_hosts()
    update_host_templates()


if __name__ == '__main__':
    main()
    # nodes = get_nodes()
    # wait_for_nodes_to_deploy(nodes)
    # update_etc_hosts()
    # update_host_templates()
