Edit the `vars` section in `smartgateway.yml`

```
ansible-playbook smartgateway.yml -i hosts -b

PLAY [ubuntu] ****************************************************************************************************
TASK [Gathering Facts] *******************************************************************************************
ok: [192.168.1.5]

TASK [Download SmartGateway] *************************************************************************************
changed: [192.168.1.5]

TASK [Unzip SmartGateway] ****************************************************************************************
changed: [192.168.1.5]

TASK [Move SmartGateway binary] **********************************************************************************
changed: [192.168.1.5]

TASK [Create Smart-Gateway directories] **************************************************************************
changed: [192.168.1.5] => (item=/var/lib/gateway/etc)
changed: [192.168.1.5] => (item=/var/lib/gateway/logs)
changed: [192.168.1.5] => (item=/var/lib/gateway/data)

TASK [Create SmartGateway configuration file] ********************************************************************
changed: [192.168.1.5]

PLAY RECAP *******************************************************************************************************
192.168.1.5                : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
