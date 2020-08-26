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
  * User: naruto (Member role)
  * Project: naruto-project
  * Domain: Default
  **Problem**:
    * Unable to retrieve projects in Horizon
4. Test 4 by Andrey
  * User: user1 (Member role) 
  * RBAC: Create, Read, Update, Delete
  * Project: default-project1
  * Namespace: project1 created
  * Domain: default
```sh
# policy
{
       "resource": {
          "verbs": ["*"],
          "resources": ["*"],
          "version": "*",
          "namespace": "project1"
        },
        "match": [
          {
            "type": "role",
            "values": ["*"]
          },
          {
            "type": "project",
            "values": ["default-project1"]
          }
        ]
      }

#stackrc
export OS_IDENTITY_API_VERSION=3
export OS_USER_DOMAIN_NAME=default
export OS_USERNAME=user1
export OS_PROJECT_DOMAIN_NAME=default
export OS_PROJECT_NAME=default-project1
export OS_PASSWORD=c0ntrail123
export OS_AUTH_URL=http://192.168.30.78:5000/v3
export OS_DOMAIN_NAME=default
```


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

Restart scenarios:
* vrouter agent
* kubelet
* kubemanager restart
  * Create pod with some User
  * Restart kubemanager
  * Earlier one should be intact
  * Deleting new Pod
  * Creating new pod
* master restart
* config_api restart
* keystone-auth-pod restart (Main)
  * Create user
  * Restart
  * After restart 
  * Add new user
* docker restart on Compute and Master

Components point of View
* Keystone restart
* User and User privileges

First admin project(admin domain): Restart 
Second non-admin project(admin domain): 
  * Just keystone and config_api

Different domain