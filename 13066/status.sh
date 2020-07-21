n20_status=$(juju status|grep noden20)
n19_status=$(juju status|grep noden19)
i34_status=$(juju status|grep nodei34)
c9_status=$(juju status|grep nodec9)
c61_status=$(juju status|grep nodec61)

while [[ ${n20_status} != *"Deployed"* ]] && [[ ${n19_status} != *"Deployed"* ]] && [[ ${i34_status} != *"Deployed"* ]] && [[ ${c9_status} != *"Deployed"* ]] && [[ ${c61_status} != *"Deployed"* ]]; do
	echo "Deploying"
	n20_status=$(juju status|grep noden20)
	n19_status=$(juju status|grep noden19)
	i34_status=$(juju status|grep nodei34)
	c9_status=$(juju status|grep nodec9)
	c61_status=$(juju status|grep nodec61)
	sleep 5
done
