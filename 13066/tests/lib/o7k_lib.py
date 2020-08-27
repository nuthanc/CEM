from keystoneclient import client as ks_client


class O7k_lib:

    def __init__(self, username=None, password=None, domain_name=None, project_name=None, auth_url=None):
        self.keystone = self.get_client()
        self.session = self.keystone.session
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.project = project_name
        self.version = '3'
        self.domain_name = domain_name or 'Default'

    def create_project(self, project_name, domain_name='Default'):
        pass

    def find_domain(self, domain_name):
        keystone.domains.find(name=domain_name)

    def get_client(self, scope='domain'):
        return ks_client.Client(version=self.version, session=self.get_session(scope), auth_url=self.auth_url, region_name=self.region_name)
