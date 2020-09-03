from lib.o7k_lib import O7kLib

admin = O7kLib(username='admin', password='password', domain_name='admin_domain',
               project_name='admin', auth_url='http://192.168.30.76:5000/v3')

# admin.create_domain('bro')
# admin.create_domain('bro')
# admin.create_project(project_name='tom_project', domain_name='tom')
# admin.create_user(user='bob', password='password', project_name='tom_project', domain_name='tom')
# admin.add_user_role(user_name='bob', role_name='admin',
#                     project_name='tom_project', domain_name='tom')
# admin.delete_user('jerry', project_name='tom_project', domain_name='tom')
# admin.delete_domain('tom')
admin.delete_domain('bro')
