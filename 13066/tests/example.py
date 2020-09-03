from lib.o7k_lib import O7kLib
from subprocess import check_output


class Example(O7kLib):
    def __init__(self, username='admin', password='password', domain_name='admin_domain', project_name='admin', auth_url=None):
        self.auth_url = self.get_auth_url() if auth_url == None else auth_url
        super().__init__(username=username, password=password,
                         domain_name=domain_name, project_name=project_name, auth_url=self.auth_url)

    def create_all(self, user_name='test_user', password='test_password', role='Member', project_name='test_project', domain_name='test_domain'):
        self.create_domain(domain_name)
        self.create_project(project_name=project_name, domain_name=domain_name)
        self.create_user(user=user_name, password=password,
                         project_name=project_name, domain_name=domain_name)
        self.add_user_role(user_name=user_name, role_name=role,
                           project_name=project_name, domain_name=domain_name)

    def delete_all(self, user_name='test_user', project_name='test_project', domain_name='test_domain'):
        self.delete_user(user_name, project_name=project_name,
                         domain_name=domain_name)
        self.delete_project(project_name)
        self.delete_domain(domain_name)

    def get_auth_url(self):
        auth_ip = check_output(
            "juju status | grep 5000 | awk '{print $5}'", shell=True, universal_newlines=True).strip()
        auth_url = f'http://{auth_ip}:5000/v3'
        return auth_url



# admin = Example(username='admin', password='password', domain_name='admin_domain',
#                project_name='admin', auth_url='http://192.168.30.76:5000/v3')

# Utilizing default values to get similar parameters as above
admin = Example()
admin.create_all('john', 'c0ntrail123', 'Member', 'new_project', 'new_domain')
admin.delete_all('john', 'new_project', 'new_domain')

# Create and Delete for test_user
admin.create_all()
admin.delete_all()
