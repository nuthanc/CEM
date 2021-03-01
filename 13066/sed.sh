auth_ip=$(juju status|grep 5000|awk '{print $5}')
auth_url=http://${auth_ip}:5000/v3
sed -i 's|auth_url: .*|auth_url: http://192.168.7.13:35357/v3|' contrail_test_input.yaml
