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