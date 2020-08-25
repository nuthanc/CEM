# Canonical JuJu Contrail CNI (K8S) Deployment Using Existing Keystone

### Description(As in story)
* It should be possible to deploy a contrail k8s cluster using JuJu on Ubuntu with keystone from an existing deployed OpenStack
* Authentication of users within the Kubernetes cluster would be performed using keystone
* To provide for enhanced cluster security the cluster kube-manager may be hosted on the Contrail controller rather than the kubernetes master
* The kube-manager should support secure remote connections to the kubernetes API server
* The integration with keystone is done on Kubernetes level using k8s-keystone-auth pod
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
* test_contrail_status
  * Test to verify that all services are running and active
* test_verify_object_logs
  * Create vn/vm and verify object log tables updated with those vn, vm and routing-instance - fails otherwise
* test_floating_ip
  * Test to validate floating-ip Assignment to a VM. It creates a VM, assigns a FIP to it and pings to a IP in the FIP VN
* test_heat_stacks_list
  * Validate installation of heat. This issues a command to list all the heat-stacks
* test_basic_snat_behavior_without_external_connectivity
  * set router-gateway to external network, launch a private network and attach it to router, validate left vm pinging right vm through Snat
* test_basic_policy_allow_deny
  * Create 2 Vns and allow icmp traffic between them and validate with pings.Update the policy to deny the same traffic.Check that pings fail
* test_sec_group_basic
  * Description: Test basic SG features
    1. Security group create and delete
    2. Create security group with custom rules and then update it for tcp
    3. Launch VM with custom created security group and verify
    4. Remove secuity group association with VM
    5. Add back custom security group to VM and verify
    6. Try to delete security group with association to VM. It should fail.
    7. Test with ping, which should fail
    8. Test with TCP which should pass
    9. Update the rules to allow icmp, ping should pass now.
* test_svc_in_network_datapath
* test_vdns_ping_same_vn
  * Test:- Test vdns functionality. On VM launch agent should dynamically update dns records to dns agent
      1.  Create vDNS server 
      2.  Create IPAM using above vDNS data 
      3.  Create VN using above IPAM and launch 2 VM's within it 
      4.  Ping between these 2 VM's using dns name 
      5.  Try to delete vDNS server which has IPAM back-reference[Negative case] 
      6.  Add CNAME VDNS record for vm1-test and verify we able to ping by alias name 
  * Pass criteria: Step 4,5 and 6 should pass
* test_vm_file_trf_scp_tests
  * Description: Test to validate File Transfer using scp between VMs. Files of different sizes.
  * Test steps:
    1. Creating vm's - vm1 and vm2 and a Vn - vn222
    2. Transfer file from vm1 to vm2 with diferrent file sizes using scp
    3. file sizes - 64,1202,2210,10000
    4. verify files present in vm2 match with the size of the file sent.
  * Pass criteria: File in vm2 should match with the transferred file size from vm1
* test_generic_link_local_service
  * Description: Test to validate generic linklocal service - running nova list from vm.
    1.*Create generic link local service to be able to wget to jenkins
    2.Create a vm
    3.Try wget to jenkins - passes if successful else fails
* test_ping_within_vn_two_vms_two_different_subnets
  * Description:  Validate Ping between 2 VMs in the same VN, 2 VMs in different VN
        subnets.
  * Test steps:
      1. Create 1 IPAM's.
      2. Create 1 VN with 2 subnets and launch 2 VMs in them.
      3. Ping between the VMs in the same VN should go thru fine.
      4. Ping to the subnet broadcast and all-broadcast address.
  * Pass criteria: VM in the same subnet will respond to both the pings, while the VM in a different VN should respond only to the all-broadcast address.

### Manual check by Anastasia
* I've checked that /etc/contrail/contrail-kubernetes.conf in kube-manager container have [AUTH] section with keystone user/password/token_url and that k8s-keystone-auth pods are running in kube-system namespace

### Solution Testing
* Should be end to end
* Can add 
* Questions:
  * When is Keystone used in Kubernetes?
  * How did you test authentication in Kubernetes using credentials from Openstack?
  * How to add Users to Keystone in Kubernetes
  * How to delete Users to Keystone in Kubernetes

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