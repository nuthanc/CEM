### Restart scenarios
* vrouter agent
* kubelet
* kubemanager restart
  * Create pod with some User
  * Restart kubemanager
  * Earlier one should be intact
  * Deleting new Pod
  * Creating new pod
* master restart
* config_api restart
* keystone-auth-pod restart (Main)
  * Create user
  * Restart
  * After restart 
  * Add new user
* docker restart on Compute and Master

### Key components
* Keystone-auth-pod restart
* User and User privileges

### Policy
* Trailing , shouldn't be there

### Tests done
* Restart scenarios with Project in Default domain and Admin domain
* Policy change with Project in Default domain
* With different domain
* With Namespace

### Tests to be done

### Tests not working
* version 2 policy
* version 2 in combination with version 1
  * Even version 1 policies don't work

https://stackoverflow.com/questions/28557626/how-to-update-yaml-file-using-python
