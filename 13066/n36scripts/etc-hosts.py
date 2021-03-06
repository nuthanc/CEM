import subprocess
import sys
import os
import yaml

TEST_INPUT = 'test_input.yaml'
localhosts = []
hosts = []
mgmt_dns = []
ctrl_dns = []
commands = []
mgmt_ips = []
ctrl_ips = []

with open(TEST_INPUT) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

nodes = list(data['instances'].keys())
for _, v in data['instances'].items():
  mgmt_ips.append(v['ip'])

# Comment control ips for single interface deployment
for _, v in data['control_data'].items():
  ctrl_ips.append(v['ip'])


for ip in mgmt_ips:
    os.system(f'ssh-keygen -f "/root/.ssh/known_hosts" -R "{ip}"')

def host_mapping():
  for i in range(len(nodes)):
    hosts.append(f"ubuntu@{mgmt_ips[i]}")
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    localhosts.append(f"127.0.1.1 {nodes[i]}.maas {nodes[i]}")
    mgmt_dns.append(f"{mgmt_ips[i]} {nodes[i]}.maas {nodes[i]}")
    if ctrl_ips[i] == "":
      ctrl_dns.append("")
    else:
      ctrl_dns.append(f"{ctrl_ips[i]} {nodes[i]}.maas {nodes[i]}")

  # print(hosts)
  # print(localhosts)
  # print(mgmt_dns)
  # print(ctrl_dns)

def mach_specific_sed_cmd():
  for i in range(len(nodes)):
    command = f"sudo sed -i"
    for j in range(len(nodes)):
      command += f" -e '/{localhosts[i]}/i {mgmt_dns[j]}'"
      if ctrl_dns[j] != "":
        command += f" -e '/{localhosts[i]}/i {ctrl_dns[j]}'"
    command += " /etc/hosts"
    commands.append(command)
  # for c in commands:
  #   print(c)
  #   print()

def execute_cmd_on_remote(i):
  ssh = subprocess.Popen(["ssh", "%s" % hosts[i], commands[i]],
                          shell=False,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
  result = ssh.stdout.readlines()
  err = ssh.stderr.readlines()
  print(result)
  print(err)

def ssh_sed(machine='all'):
  if machine == 'all':
    for i in range(len(nodes)):
      execute_cmd_on_remote(i)
  else:
    execute_cmd_on_remote(machine)


host_mapping()
mach_specific_sed_cmd()
# By default on all machines if no parameter is specified
ssh_sed()
# ssh_sed(machine=3)
# ssh_sed(machine=4)
# ssh_sed(machine=0)
# ssh_sed(machine=2)
