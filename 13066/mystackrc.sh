export OS_IDENTITY_API_VERSION=3
export OS_USER_DOMAIN_NAME=admin_domain
export OS_USERNAME=user_k8s_nuthan
export OS_PROJECT_DOMAIN_NAME=admin_domain
export OS_PROJECT_NAME=k8s
export OS_DOMAIN_NAME=admin_domain
export OS_PASSWORD=password
export OS_AUTH_URL=http://192.168.30.78:5000/v3


# openstack domain create --description "nuthan Domain" nuthan
# openstack project create --description "nuthan project" nuthan_project --domain nuthan
# openstack user create --project nuthan_project --password  c0ntrail123 --domain nuthan nuthan_user

openstack project create --description "nuthan k8s project" --domain admin_domain k8s
openstack user create --project k8s --project-domain admin_domain --password password --domain admin_domain user_k8s_nuthan

openstack project create --description "k8s with se1 namespace" --domain admin_domain k8s1-se1
openstack user create --project k8s1-se1 --project-domain admin_domain --password password --domain admin_domain k8s1-se1-user
export OS_USERNAME=k8s1-se1-user
export OS_PROJECT_NAME=k8s1-se1
# Role not set, try setting role


openstack user create --project bd8b1f3cbe964974b7b9e0d997dfecd7 --project-domain admin_domain --password password --domain admin_domain nuthan_admin2
openstack role add --user nuthan_admin2 --user-domain admin_domain --project admin --project-domain admin_domain admin

export OS_USERNAME=nuthan_admin2
export OS_PROJECT_NAME=bd8b1f3cbe964974b7b9e0d997dfecd7
export OS_IDENTITY_API_VERSION=3
export OS_USER_DOMAIN_NAME=admin_domain
export OS_PROJECT_DOMAIN_NAME=admin_domain
export OS_DOMAIN_NAME=admin_domain
export OS_PASSWORD=password
export OS_AUTH_URL=http://192.168.30.78:5000/v3

