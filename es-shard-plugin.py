from math import pow
import collectd
import urllib2
import json
import re

PLUGIN_NAME = 'elasticsearch-shard-monitor'
INTERVAL = 10  # seconds
_host = None
_port = None

def configure(config_obj):
    '''Example configuration:

    - type: collectd/custom
        template: |
          LoadPlugin "python"
          <Plugin python>
            ModulePath "/usr/lib/signalfx-agent/lib/python2.7/"
            Import "elasticsearch_shard_monitor"
            <Module "elasticsearch_shard_monitor">
                Interval "5"
            </Module>
          </Plugin>
    '''

    global _host
    global _port

    config = {c.key: c.values[0] for c in config_obj.children}

    _host = config.get('Host')           or 'localhost'
    _port = config.get('Port')           or 9200


def request(endpoint):
    url = 'http://' + _host + ':' + str(_port) + endpoint
    req = urllib2.Request(url)
    response = urllib2.urlopen(req) # Throw on failure
    return response.read()


def get_cluster_name():
    res = request('/_cluster/health')
    parsed = json.loads(res)
    return parsed.get('cluster_name')


def get_shard_data():
    res = request('/_cat/shards?h=index,shard,prirep,state,store,node')
    rows = res.split('\n')
    data = filter(None, map(parse_rows, rows))
    return data


def parse_rows(row):
    fields = row.split()

    if (fields == None or len(fields) != 6):
        return None

    data = {
        'index': fields[0],
        'shard_number': fields[1],
        'shard_id': fields[0] + "_" + fields[1] + "_" + fields[5], # There's no unique ID here, so ID is generated as index_shard_host
        'prirep': fields[2],
        'shard_state': fields[3],
        'shard_size': get_bytes(fields[4])
    }

    return data


def get_bytes(size):
    power = 1024
    multipliers = {'b': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    suffix = re.sub(r'[0-9\.]', '', size)
    value = size.replace(suffix, '')
    return int(float(value) * pow(power, multipliers.get(suffix)))


def get_node_id():
    res = request('/_nodes/_local')
    parsed = json.loads(res)
    id = parsed.get("nodes").keys()[0]
    return id


def get_master_id():
    res = request('/_cluster/state/master_node')
    parsed = json.loads(res)
    id = parsed.get("master_node")
    return id


def format_dimensions(shard, cluster):
    del shard['shard_size']
    shard['cluster'] = cluster
    shard['plugin_instance'] = cluster
    dim_pairs = ["%s=%s" % (k, v) for k, v in shard.iteritems()]

    return "[%s]" % (",".join(dim_pairs))


def read(data=None):
    node_id = get_node_id()
    master_id = get_master_id()

    # Only report from master to reduce messages sent
    if (node_id != master_id):
        print("I'm not master, skipping...")
        return

    shard_data = get_shard_data()
    cluster = get_cluster_name()

    for shard in shard_data:
        val = collectd.Values(type='gauge', type_instance="cluster.shards.size")
        val.plugin = PLUGIN_NAME
        val.values = (shard.get('shard_size'),)
        val.plugin_instance = format_dimensions(shard, cluster)
        val.dispatch()

collectd.register_config(configure)
collectd.register_read(read, INTERVAL)
