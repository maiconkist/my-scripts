- Add the corresponding lora-server and lora-client  to your ~/.ssh/config file
- Change all 'ansible_ssh_common_args'  to point to your ~/.ssh/config file.


Exec ansible-playbook with:
```
ansible-playbook -i hosts install.yaml
```
