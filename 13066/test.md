### What was tested

1. Test 1
  * User: nuthan_admin2
  * Project: admin
  * Domain: admin_domain
  * Namespace: default
  * Verbs: get, create
2. Test 2
  * User: 


Admin project:
Non-admin project: User creation, admin role
  * Create pods
  * Delete pods
  * Create deployments and Delete
  * Create service and Delete
  * Create daemonset and Delete
  * CRD: NetworkAttachmentDefinition and Delete

Non-admin role: Creation k8s objects
Admin user should be able to delete pods of non-admin User
RBAC