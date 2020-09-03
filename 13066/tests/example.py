from lib.o7k_lib import O7kLib

admin = O7kLib(username='admin', password='password', domain_name='admin_domain',
               project_name='admin', auth_url='http://192.168.30.76:5000/v3')


def create_all(user_name, password, role, project_name='admin', domain_name='admin_domain'):
    admin.create_domain(domain_name)
    admin.create_project(project_name=project_name, domain_name=domain_name)
    admin.create_user(user=user_name, password=password,
                      project_name=project_name, domain_name=domain_name)
    admin.add_user_role(user_name=user_name, role_name=role,
                        project_name=project_name, domain_name=domain_name)


def delete_all(user_name, project_name='admin', domain_name='admin_domain'):
    admin.delete_user(user_name, project_name=project_name,
                      domain_name=domain_name)
    admin.delete_project(project_name)
    admin.delete_domain(domain_name)


# create_all('john', 'c0ntrail123', 'Member', 'new_project', 'new_domain')
delete_all('john', 'new_project', 'new_domain')
