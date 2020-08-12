### Process of running Sanity in Juju based setup

```sh
git clone https://github.com/tungstenfabric/tf-dev-test

# Export the below(Did it in controller(n20))
export ORCHESTRATOR=all
export CONTROLLER_NODES="192.168.30.20, 192.168.30.29, 192.168.30.34"
export AGENT_NODES="192.168.30.9,192.168.30.19"
export SSH_USER=root
# export CONTAINER_REGISTRY="bng-artifactory.juniper.net/contrail-nightly"
export TF_TEST_IMAGE="bng-artifactory.juniper.net/contrail-nightly/contrail-test-test:2008.46"
export CONTRAIL_CONTAINER_TAG=2008.46
# export SSL_ENABLE=True
export SSL_ENABLE=false
export DEPLOYER=juju
export OPENSTACK_VERSION=queens
export AUTH_PASSWORD=password
export AUTH_DOMAIN=admin_domain
export AUTH_REGION=RegionOne
export AUTH_URL="http://192.168.30.187:35357/v3"
export AUTH_PORT=35357

# Allow RootLogin in all of the nodes
sudo su
passwd root
# In /etc/ssh/sshd_config, PermitRootLogin yes and PasswordAuthentication yes
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd

./tf-dev-test/contrail-sanity/run.sh
```

### Note 

* Andrey told that tf-dev-test doesn’t have support of deployments where components of control plane are separated to different nodes

### Manual sanity

```sh
bash -x run_tests.sh -m -U -T ci_sanity -t
```