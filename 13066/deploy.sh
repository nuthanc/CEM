set -x
juju add-model default
juju model-config default-space=mgmt
set +x
nohup bash juju_deploy_status_etch.sh &
