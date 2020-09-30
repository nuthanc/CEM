# Canonical JuJu Contrail CNI (K8S) Deployment Using Existing Keystone

### Description(As in story)
* It should be possible to deploy a contrail k8s cluster using JuJu on Ubuntu with keystone from an existing deployed OpenStack
* Authentication of users within the Kubernetes cluster would be performed using keystone
* To provide for enhanced cluster security the cluster kube-manager may be hosted on the Contrail controller rather than the kubernetes master
* The kube-manager should support secure remote connections to the kubernetes API server
* The integration with keystone is done on Kubernetes level using k8s-keystone-auth pod
* [Steps given by Andrey](https://github.com/nuthanc/CEM/blob/master/13066/attached_files/steps.md)
* [Check the attached k8s.md which contains detailed explanation](https://github.com/nuthanc/CEM/blob/master/13066/attached_files/k8s.md)

### Keywords
* Keystone from Existing Deployed Openstack cluster
* k8s+o7k+Contrail
* Contrail controller relation with Openstack and Kubernetes
* Keystone webhook
  * k8s-keystone-auth Deployment in kube-system namespace

### Workflow explanation from Danil
* [Important links](#Important-links-for-Keystone-webhook)
* https://web.microsoftstream.com/video/ca542822-7b61-41fa-a87e-27ddb7e74750
* A Webhook is an HTTP callback; http post to an URL when something happens
* Important Requirement:
  * Authorization policy
* k8s-keystone-auth is the middleman between K8s API and Keystone
* In master node, ps -ef | grep api
  * In this command, we see Auth mode as Webhook, along with webhook-config-file
  * The webhook config file denotes the server to which API should send Authentication and Authorization requests
* When User comes to the API and authenticates with Keystone token, the API will get the token and send it to the Webhook
* On master, kubectl get svc -n kube-system
  * k8s-keystone-auth-service has the same clusterip mentioned in the webhook config file
* API knows where to send Authorization commands, so that Keystone can validate the token and get back if the Token was valid or not
* On the master, kube-proxy is running which takes of creating IPtable rules to translate destination address to actual pod address
  * iptables -L -n -t nat | grep <webhook-service-ip>
* 8:32 ipfabric forwarding enable in K8s(Packets coming from the master nodes can reach the pods)
* juju config kubernetes-master keystone-policy
  * This is the default configuration option
  * This has to be changed
* The above config gets created as a ConfigMap
  * kubectl get cm -n kube-system
  * kubectl ger cm -n kube-system -o yaml k8s-auth-policy
* Create policy file containing the above contents and append required config
  * Check the policy.yaml file
* juju config kubernetes-master keystone-policy="$(cat policy.yaml)"
* To check the ports to which the master is listenining
  * ss -tupln | grep 6443
* Now, there should be a rule in the iptables
  * iptables -L -n -t nat | grep <webhook-service-ip>
* kubectl config use-context keystone
  * source rc file
  * openstack server list
  * kubectl get pods
* Prereq:
  * Installed kubectl on Jumphost(snap install kubectl --classic)
  * Copied config file from master to ~/.kube/config
  * snap install --edge client-keystone-auth
* To check if token is being sent to keystone
  * tcpdump -Anni any "host <keystone-ip> and port 5000"
  * Do kubectl get pods and then execute the above(Both cmds in jumphost)


### Users in Kubernetes
* https://kubernetes.io/docs/reference/access-authn-authz/authentication/#users-in-kubernetes
* Service accounts: https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/
  * Google Search: Configure Service Accounts for Pods
* Two types of Users:
  * Normal Users: Require outside independent service like Keystone or Google accounts
  * Service accounts Users

### Tests done in Feature test
* Openstack ci_sanity: https://gist.github.com/nuthanc/403ecac640522dd3219b8678802f7ae9
* k8s ci_sanity

### Manual check by Anastasia
* I've checked that /etc/contrail/contrail-kubernetes.conf in kube-manager container have [AUTH] section with keystone user/password/token_url and that k8s-keystone-auth pods are running in kube-system namespace

### Solution Testing
* https://contrail-jws.atlassian.net/browse/CEM-17392

### Questions to ask Andrey
* How is authentication handled for k8s pods in joint cluster of Openstack and Kubernetes

### Ticktick comments
```txt
3 ha, os , contrail , kubemanger
Openstack n20: no ha if not sufficient
i34 as controller: 
c9 or c61 as compute: k8s compute
https://contrail-jws.atlassian.net/browse/CEM-13066

UI point of view: 
Authentication going through keystone
Negative test cases

Ask: Clarify import to UI

Requirement: UI import support
API 
Blueprint: Entry point for each feature
Logs to authentication to 
Create pod 
POd authentication to keystone: 
Bring down keystone 
authentication shouldn't require

Why there is not a UI support 
Understand the Process
```

### Mistakes in bundle file
* First thing - cluster must container odd number of nodes. two nodes don’t have a quorum and can’t build cluster
* Secondly - it’s not possible to place openstack units to the same machine. they don’t work in this way. only lxd containers are possible
* In general it’s better to separate contrail-control plane and kubernetes-master to different machines
  * This is because along with kubernetes-master, vrouter is also installed according to Andrey

### Question for HA
* For the User story 13066, what kind of HA testing is expected?
  * Openstack HA: But this is difficult
    *  Need to add ceph as a shared storage for cinder, glance, nova and also add VIP-s and hacluster for all of them
  * Contrail HA: Controller, Analytics and Analyticsdb
  * Kubernetes HA: Master HA but it shouldn't be on the same machine as the Contrail Control plane
* How many machines will be required 
* Andrey answered that in Production
```sh
I can suggest that HA is not required there

1 machine for contrail control plane
1 machine for openstack control plane
1 machine for kubernetes master
1 machine for nova compute
1 machine for kubernetes worker

it a minimal configuration that is close to production
contrail’s control plane and openstack control plane can be the same machine if it’s big enough
you can make contrail HA but openstack not HA and many other combinations
```

### Discussion with Venky

```txt
Cluster level authentication

Authentication is for the nodes

Any user who logs in to Openstack, must be able to create Pods

Keystone

Not Deployment level but User level


NO authentication at the User level
Contrail does not support more than 1 User for k8s

Rights given by Keystone.

Pod creation, how is the flow


Nested: Openstack underlya


Nested:
vms created on top of Openstack and top of this we create a k8s cluster


Where and all to check?
What to check?

Testcase for keystone auth for k8s using a particular User

Workflow from 
```

### Important links for Keystone webhook
* https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/using-keystone-webhook-authenticator-and-authorizer.md
* https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/using-keystone-webhook-authenticator-and-authorizer.md#test-k8s-keystone-auth-service
* https://ubuntu.com/kubernetes/docs/ldap

### Yuvaraja debug
* https://web.microsoftstream.com/video/1ceeac08-ca4d-44ee-a97f-64d5a15bfd81
```sh
setting->config_editor->vmi delete vhost0 nodec9
dmesg


free -g
top 
/var/log/syslog
/var/log/pods/kube-system../

flow -l
vif --list
vrouter machine
docker restart vrouter_provisioner_1

k exec -it vrouter_agent bash

vif --list
(Now it has i-address)

ping -I vhost0 <pod-ip> should work
route -n
tcpdump -nei vhost0 <ubuntu-pod-ip>
Simultaneousy ping
ARP should not happen

ping google.com
tcpdump -nei vhost0 <google-ip>
nodec9
ip route del 10.32.0.0/12
Don't configure vrouter_gateway in single interface

Restart 28 for cordns, shouldn't be any restart

Host to one of the pod ip in the overlay
Ping ubuntu ip from the host
It should not fail
Deleted the ip route rule
Underlay to overlay

```

### Need to do for multi-interface
```sh
juju add-space data
juju move-to-space 192.168.40.0/24

# In bundle file, bindings under kubernetes-worker
```