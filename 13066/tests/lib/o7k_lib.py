from keystoneclient import client as ks_client
from keystoneauth1 import identity as ks_identity
from keystoneauth1 import session as ks_session
from subprocess import check_output

class O7kLib:

    def __init__(self, username=None, password=None, domain_name=None, project_name=None, auth_url=None, cert=None, key=None, cacert=None, insecure=True, region_name=None, scope='domain'):
        self.version = '3'
        self.sessions = dict()
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.project = project_name
        self.domain_name = domain_name or 'Default'
        self.cert = cert
        self.key = key
        self.cacert = cacert
        self.insecure = insecure
        self.region_name = region_name
        self.scope = scope
        self.keystone = self.get_client(self.scope)

    def get_client(self, scope='domain'):
        return ks_client.Client(version=self.version, session=self.get_session(scope), auth_url=self.auth_url, region_name=self.region_name)

    def get_session(self, scope='domain'):
        if scope in self.sessions:
            return self.sessions[scope]

        project_name = None if scope == 'domain' else self.project
        project_domain_name = None if scope == 'domain' else self.domain_name
        domain_name = self.domain_name if scope == 'domain' else None
        self.auth = ks_identity.v3.Password(auth_url=self.auth_url,
                                            username=self.username,
                                            password=self.password,
                                            project_name=project_name,
                                            domain_name=domain_name,
                                            user_domain_name=self.domain_name,
                                            project_domain_name=project_domain_name)

        self.sessions[scope] = ks_session.Session(auth=self.auth,
                                                  verify=not self.insecure if self.insecure else self.cacert,
                                                  cert=(self.cert, self.key))
        return self.sessions[scope]

    def find_domain(self, domain_name):
        return self.keystone.domains.find(name=domain_name)

    def find_project(self, project_name):
        return self.keystone.projects.find(name=project_name)

    def user_list(self, project_name=None, domain_name=None):
        project = self.find_project(project_name)
        domain = self.find_domain(domain_name)
        return self.keystone.users.list(project=project, domain=domain)
        # self.keystone.users.list(project=self.keystone.projects.find(
            # name='nuthan-project'), domain=self.keystone.domains.find(name='nuthan'))

    def get_user_dct(self, user_name, project_name=None, domain_name=None):
        all_users = self.user_list(project_name, domain_name)
        for x in all_users:
            if (x.name == user_name):
                return x
        return None

    def roles_list(self):
        return self.keystone.roles.list()

    def get_role_dct(self, role_name):
        all_roles = self.roles_list()
        for x in all_roles:
            if (x.name == role_name):
                return x
        return None

    def tenant_list(self, limit=None, marker=None):
        return self.keystone.projects.list()

    def get_tenant_dct(self, project_name):
        all_tenants = self.tenant_list()
        for x in all_tenants:
            if (x.name == project_name):
                return x
        return None

    def create_project(self, project_name, domain_name='Default'):
        if not self.keystone.projects.find(name=project_name):
            domain = self.find_domain(domain_name)
            self.keystone.projects.create(name=project_name, domain=domain)
        else:
            print(f"Project {project_name} already present, not creating")

    def create_domain(self, domain_name):
        if not self.find_domain(self.domain_name):
            self.keystone.domains.create(domain_name)
        else:
            print(f"Domain {domain_name} already present, not creating")

    def create_role(self, role):
        self.keystone.roles.create(role)

    def create_user(self, user, password, email='', project_name=None,
                    enabled=True, domain_name=None):
        project_id = self.get_tenant_dct(project_name).id
        domain_id = self.find_domain(domain_name).id
        self.keystone.users.create(
            user, domain_id, project_id, password, email, enabled=enabled)
    
    def delete_project(self, name, obj=None):
        if not obj:
            obj = self.keystone.projects.find(name=name)
        self.keystone.projects.delete(obj)

    def update_domain(self, domain_id, domain_name=None,
                      description=None, enabled=None):
        return self.keystone.domains.update(domain=domain_id, name=domain_name,
                                            description=description,
                                            enabled=enabled)
    
    def delete_domain(self, domain_name, domain_obj=None):
        if not domain_obj:
            domain_obj = self.find_domain(domain_name)
        self.update_domain(domain_id=domain_obj.id, enabled=False)
        return self.keystone.domains.delete(domain_obj)

    def add_user_role(self, user_name, role_name, project_name=None, domain_name=None):
        check_output("")
        #TODO Need to add user role
    
admin = O7kLib(username='admin', password='password', domain_name='admin_domain',
            project_name='admin', auth_url='http://192.168.30.76:5000/v3')

admin.create_domain('nuthan')
admin.create_project(project_name='nuthan_project', domain_name='nuthan')
admin.create_user(user='rovanova', password='c0ntrail123', project_name='nuthan_project', domain_name='nuthan')
admin.add_user_role(user_name='rovanova', role_name='Member', project_name='nuthan_project', domain_name='nuthan')
