from flask import Flask, json, render_template
from pycontrolshed.model import Environment
from werkzeug.contrib.cache import SimpleCache
import pycontrolshed

app = Flask(__name__)
app.config.from_object(__name__)

bigips = {}
cache = SimpleCache()
pyctrl_config = pycontrolshed.get_configuration()

def create_ltm(environment_name):
    environ = Environment(environment_name)
    environ.configure(pyctrl_config)
    return environ.active_bigip_connection

def get_ltm(environment_name):
    if not bigips.has_key(environment_name):
        bigips[environment_name] = create_ltm(environment_name)
    return bigips[environment_name]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/env.json')
def env_list_json():
    response = {'environments': []}
    for name in pyctrl_config.sections():
        if name == 'global_options':
            pass
        else:
            ltm = get_ltm(name)
            environment = {'name': name}
            environment['partitions'] = [p['name'] for p in ltm.partitions]
            response['environments'].append(environment)
    return json.dumps(response)
        

@app.route('/<environment>.json')
def environment_json(environment):
    print "%s" % environment

@app.route('/<environment>/<partition>.json')
def partition_json(environment, partition):
    bigip = get_ltm(environment)
    bigip.active_partition = partition
    partition_data = {'name': partition,
                      'children': []}

    pools = bigip.pools.pools()
    if len(pools):
        status_data = bigip.pools.members(pools)
        stats_data = bigip.pools.multi_member_statistics(pools, status_data)

        for pool_name in status_data.keys():
            pool = {'name': pool_name,
                    'children': []}
            partition_data['children'].append(pool)
            for pool_datum in status_data[pool_name]['members']:
                monitor = pool_datum['monitor']
                address = "%s:%d" % (monitor.member.address, monitor.member.port)
                status = monitor.monitor_status
                stats = stats_data[pool_name][address]
                pool['children'].append({'address': address,
                                         'status': status,
                                         'stats': stats})
    return json.dumps(partition_data)


