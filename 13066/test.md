### What was tested

* Domain should be same as default-domain in contrail
* Combinations which I need to test
  * Admin domain and nuthan project
  * 
1. Test 1
  * User: nuthan_admin2 (admin role)
  * Project: admin
  * Domain: admin_domain
    * Namespace: default and kirthan(Created only cirros pod here)
    * Verbs: get, create
2. Test 2
  * User: nuthan_demo2 (admin role)
  * Project: demo_project
  * Domain: admin_domain
  **Problem**:
    * Unable to retrieve projects in Horizon
    * Attempt to retrieve pods
```sh
Invalid user credentials were provided
I0825 08:14:29.316271   30362 helpers.go:234] Connection error: Get https://192.168.30.29:6443/api/v1/namespaces/default/pods?limit=500: getting credentials: exec plugin didn't return a token or cert/key pair
F0825 08:14:29.316377   30362 helpers.go:115] Unable to connect to the server: getting credentials: exec plugin didn't return a token or cert/key pair

openstack user list --domain admin_domain --project demo_project
+----------------------------------+--------------+
| ID                               | Name         |
+----------------------------------+--------------+
| e3b62476a91c441b8debda1c8f987dc8 | nuthan_demo2 |
+----------------------------------+--------------+
```
3. Test 3
  * User: nuthan_demo3 (admin role)
  * Project: k8s
  * Domain: Default
  **Problem**:
    * Unable to retrieve projects in Horizon
4. Test 4
  * User: nuthan_demo (Member role)
  * Project: demo_project
  * Domain: admin_domain


Admin project:
Non-admin project: User creation, admin role
  * Create pods and Delete
  * Create deployments and Delete
  * Create service and Delete
  * Create daemonset and Delete
  * Create CRD: NetworkAttachmentDefinition and Delete

Non-admin role: Creation k8s objects
Admin user should be able to delete pods of non-admin User
RBAC