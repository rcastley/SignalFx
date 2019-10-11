import sys
import requests
import json
import time
import logging

# - type: python-monitor
#   intervalSeconds: 60
#   scriptFilePath: "/usr/local/scripts/pingdom.py"
#   api_key: "PINGDOM_API_KEY"
#   user: "YOUR_PINGDOM_USERNAME"
#   password: "YOUR_PINGDOM_PASSWORD"

logger = logging.getLogger(__name__)

def call_api(api, api_key, user, password):
  headers = {
    'App-Key': api_key
  }
  base_api = 'https://api.pingdom.com/api/2.0/' + api
  response = requests.get(base_api, headers = headers, auth = requests.auth.HTTPBasicAuth(user, password))
  if response.status_code == 200:
    return response.json()
  else :
    logger.error("API [" + base_api + "] failed to execute with error code [" + str(response.status_code) + "].")

def run(config, output):
  api_key = config.get("api_key")
  user = config.get("user")
  password = config.get("password")
  response = call_api('checks', api_key, user, password)

  data = response.get("checks")

  counts = response.get("counts")

  up_count = 0
  down_count = 0
  unconfirmed_down_count = 0
  unknown_count = 0
  paused_count = 0

  for x in data:
    status = x.get("status")
    output.send_cumulative("pingdom.responseTime", x.get("lastresponsetime"), {"hostname" : x.get("hostname"), "source": "pingdom"})
    if status == "up":
      up_count = up_count + 1
    elif status == "down":
      down_count == down_count + 1
    elif status == "unconfirmed_down":
      unconfirmed_down_count = unconfirmed_down_count + 1
    elif status == "unknown":
      unknown_count = unknown_count + 1
    elif status == "paused":
      paused_count = paused_count + 1

  output.send_gauge("pingdom.up", up_count, {"source": "pingdom"})
  output.send_gauge("pingdom.down", down_count, {"source": "pingdom"})
  output.send_gauge("pingdom.unconfirmed_down", unconfirmed_down_count, {"source": "pingdom"})
  output.send_gauge("pingdom.unknown", unknown_count, {"source": "pingdom"})
  output.send_gauge("pingdom.paused", paused_count, {"source": "pingdom"})
  output.send_gauge("pingdom.total", counts.get("total"), {"source": "pingdom"})
