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

def get_partition_list(environment_name):
    cache_key = '%s#partition_list' % environment_name
    pl = cache.get(cache_key)
    if pl is None:
        print "Refreshing %s cache" % cache_key
        ltm = get_ltm(environment_name)
        pl = [p['name'] for p in ltm.partitions]
        cache.set(cache_key, pl, timeout=60*60)
    return pl

def get_partition_data(env_name, partition):
    cache_key = "%s.%s" % (env_name, partition)
    pd = cache.get(cache_key)
    if pd is None:
        print "Refreshing %s cache" % cache_key
        bigip = get_ltm(env_name)
        bigip.active_partition = partition
        pd = {'name': partition,
                          'children': []}

        pools = bigip.pools.pools()
        if len(pools):
            status_data = bigip.pools.members(pools)
            stats_data = bigip.pools.multi_member_statistics(pools, status_data)

            for pool_name in status_data.keys():
                pool = {'name': pool_name,
                        'children': []}
                pd['children'].append(pool)
                for pool_datum in status_data[pool_name]['members']:
                    monitor = pool_datum['monitor']
                    address = "%s:%d" % (monitor.member.address, monitor.member.port)
                    status = monitor.monitor_status
                    stats = stats_data[pool_name][address]
                    pool['children'].append({'address': address,
                                             'status': status,
                                             'stats': stats})
        cache.set(cache_key, pd, timeout=2*60)
    return pd

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
            environment['partitions'] = get_partition_list(name)
            response['environments'].append(environment)
    return json.dumps(response)
        

@app.route('/<environment>.json')
def environment_json(environment):
    print "%s" % environment

@app.route('/<environment>/<partition>.json')
def partition_json(environment, partition):
    pd = get_partition_data(environment, partition)
    return json.dumps(pd)


