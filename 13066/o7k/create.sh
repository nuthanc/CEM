set -x
openstack  project create --domain ${DOMAIN_NAME} ${PROJECT_NAME}
openstack user create ${USERNAME} --domain ${DOMAIN_NAME} --password ${PASSWORD} --project ${PROJECT_NAME}
openstack role add --project ${PROJECT_NAME} --project-domain ${DOMAIN_NAME} --user ${USERNAME} --user-domain ${DOMAIN_NAME} ${ROLE}

openstack role assignment list --names
openstack user list --domain ${DOMAIN_NAME} --project ${PROJECT_NAME}