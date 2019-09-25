# Zabbix Plugin

# Returns data from Zabbix API
# Author: Robert Castley
# Version: 0.1
# Date: 25/09/19

# Example configuration:

# - type: python-monitor
#   scriptFilePath: "/usr/local/scripts/zabbix.py"
#   auth: "7b38879902e6b234d48acf5951cec387"

import json
import requests
import logging

logger = logging.getLogger(__name__)

def zabbix_host_get(auth):
    z_endpoint = 'http://192.168.64.13/zabbix/api_jsonrpc.php'

    z_headers = {
        'Content-Type' : 'application/json-rpc'
    }

    z_data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "countOutput" : 1
        },
        "id": 2,
        "auth": auth
}

    r = requests.post(z_endpoint, headers=z_headers, json=z_data)
    return r.content

def run(config, output):
    auth = config.get("auth")
    y = zabbix_host_get(auth)
    x = json.loads(y)
    output.send_gauge("zabbix.hosts", x["result"], {"source": "zabbix"})
