import os
import yaml
from subprocess import check_output
from jinja2 import Environment, FileSystemLoader


DEPLOY_FILE = 'my-k8s-os-mi.yaml'
TEST_INPUT = 'test_input.yaml'

def add_model():
    os.system('juju add-model default')
    os.system('juju model-config default-space=mgmt')


def prepare_yaml():
    version = input("Enter contrail version: ")
    auth_ip = check_output("juju status|grep 5000|awk '{print $5}'", shell=True, universal_newlines=True).strip()

    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
    env = Environment(loader=FileSystemLoader(THIS_DIR))

    template = env.get_template(f"{DEPLOY_FILE}.j2")
    with open(DEPLOY_FILE, 'w') as f:
        f.write(template.render(version=version))

    template = env.get_template(f"{TEST_INPUT}.j2")
    with open(TEST_INPUT, 'w') as f:
        f.write(template.render(version=version, auth_ip=auth_ip))


def get_nodes():
    with open(TEST_INPUT) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return list(data['instances'].keys())


def deploy_with_yaml():
    os.system('juju deploy ./my-k8s-os-mi.yaml')


def wait_for_nodes_to_deploy():
    import juju
    # MSG START here


def main():
    add_model()
    prepare_yaml()
    deploy_with_yaml()
    nodes = get_nodes()
    wait_for_nodes_to_deploy(nodes)
    update_etc_hosts()
    update_host_templates()


if __name__ == '__main__':
    # main()
    # prepare_yaml()
    nodes = get_nodes()
    wait_for_nodes_to_deploy(nodes)
