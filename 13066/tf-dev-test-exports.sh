export ORCHESTRATOR=all
export CONTROLLER_NODES=192.168.7.20
export AGENT_NODES="192.168.7.9,192.168.30.34"
export SSH_USER=root
# export CONTAINER_REGISTRY="bng-artifactory.juniper.net/contrail-nightly"
export TF_TEST_IMAGE="bng-artifactory.juniper.net/contrail-nightly/contrail-test-test:2008.20"
export CONTRAIL_CONTAINER_TAG=2008.20
export SSL_ENABLE=True
export SSL_ENABLE=false
export DEPLOYER=juju
export OPENSTACK_VERSION=queens
export AUTH_PASSWORD=password
export AUTH_DOMAIN=admin_domain
export AUTH_REGION=RegionOne
export AUTH_URL="http://192.168.7.120:35357/v3"
export AUTH_PORT=35357