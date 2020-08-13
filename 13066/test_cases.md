### Openstack Failed test cases
* Ubuntu image problem 
* Commented ones are Passed on Rerun
```sh
analyticstestsanity.log:2020-08-12 14:46:43,201 - INFO - END TEST : test_contrail_status : FAILED[0:01:32]
{'192.168.30.29': {'contrail-kube-manager': {'status': 'inactive', 'description': None}}})
SecurityGroupBasicRegressionTests1.test_sec_group_basic[cb_sanity,ci_contrail_go_kolla_ocata_sanity,ci_sanity,rerun,sanity,suite1,vcenter]: FAILED[]
```
{'log': <logging.Logger object at 0x7fdb7bc03690>, '_force_refresh': False, 'ame': {u'href': u'http://192.168.30.29:8081/analytics/uves/virtual-network/__UNKNOWN__?flat', u'name': u'__UNKNOWN__'}, 'base_url': '/', '_port': '8081', '_protocol': 'http', '_drv': <tcutils.verification_util.JsonDrv object at 0x7fdb7a156790>, '_ip': '192.168.30.29'}

### Openstack Passed test cases
```sh
testheat.log:2020-08-12 14:46:23,144 - INFO - END TEST : test_heat_stacks_list : PASSED[0:01:02]
analyticsbasictestsanity.log:2020-08-12 14:46:43,200 - INFO - END TEST : test_verify_object_logs : PASSED[0:01:30]
testroutersbasic.log:2020-08-12 14:48:53,441 - INFO - END TEST : test_basic_snat_behavior_without_external_connectivity : PASSED[0:02:01]
testbasicvmvn.log:2020-08-12 14:53:44,096 - INFO - END TEST : test_generic_link_local_service : PASSED[0:01:33]
testbasicvmvn.log:2020-08-12 14:56:54,767 - INFO - END TEST : test_ping_within_vn_two_vms_two_different_subnets : PASSED[0:03:10]
```