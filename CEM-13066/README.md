# Canonical JuJu Contrail CNI (K8S) Deployment Using Existing Keystone

### Description(As in story)
* It should be possible to deploy a contrail k8s cluster using JuJu on Ubuntu with keystone from an existing deployed OpenStack
* Authentication of users within the Kubernetes cluster would be performed using keystone
* To provide for enhanced cluster security the cluster kube-manager may be hosted on the Contrail controller rather than the kubernetes master
* The kube-manager should support secure remote connections to the kubernetes API server
* The integration with keystone is done on Kubernetes level using k8s-keystone-auth pod

### Keywords
* Keystone from Existing Deployed Openstack cluster
* k8s+o7k+Contrail
* Contrail controller relation with Openstack and Kubernetes

### Tests done in Feature test
* 

### Manual check by Anastasia
* I've checked that /etc/contrail/contrail-kubernetes.conf in kube-manager container have [AUTH] section with keystone user/password/token_url and that k8s-keystone-auth pods are running in kube-system namespace