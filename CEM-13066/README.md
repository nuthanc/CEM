# Canonical JuJu Contrail CNI (K8S) Deployment Using Existing Keystone

### Description(As in story)
* It should be possible to deploy a contrail k8s cluster using JuJu on Ubuntu with keystone from an existing deployed OpenStack
* Authentication of users within the Kubernetes cluster would be performed using keystone
* To provide for enhanced cluster security the cluster kube-manager may be hosted on the Contrail controller rather than the kubernetes master
* The kube-manager should support secure remote connections to the kubernetes API server

### Keywords
* Keystone
* k8s+o7k+Contrail