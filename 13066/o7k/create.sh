openstack  project create --domain ${OS_DOMAIN_NAME} ${OS_PROJECT_NAME}
openstack user create ${OS_USERNAME} --domain ${OS_DOMAIN_NAME} --password ${OS_PASSWORD} --project ${OS_PROJECT_NAME}
openstack role add --project ${OS_PROJECT_NAME} --project-domain ${OS_DOMAIN_NAME} --user ${OS_USERNAME} --user-domain ${OS_DOMAIN_NAME} ${OS_ROLE}