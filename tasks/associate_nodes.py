from cloudify import ctx
from cloudify.state import ctx_parameters as params

import sys
import os
import json
import string
from random import choice

try:
    import connection  # FIXME
except ImportError:
    sys.path.insert(0, 'lib/python2.7/site-packages/plugin/')
    import connection


node_instance = {}
kwargs = {}
kwargs['name'] = params.minion_id

if 'minions' not in ctx.instance.runtime_properties:
    ctx.instance.runtime_properties['minions'] = []
ctx.instance.runtime_properties['minions'].append(kwargs['name'])

client = connection.MistConnectionClient(properties=ctx.node.properties)
machine = client.other_machine(kwargs)

print('=======================')
print(machine.info)
print('=======================')

node_instance['node_id'] = 'kube_worker'
node_instance['name'] = 'kube_worker'
node_instance['id'] = 'kube_worker' + ''.join(choice(string.letters + string.digits) for _ in range(5))
node_instance['host_id'] = 'kube_worker' + ''.join(choice(string.letters + string.digits) for _ in range(5))
node_instance['version'] = 9
node_instance['state'] = 'started'
node_instance['runtime_properties'] = {
    'info': {
        'can_start': machine.info['can_start'],
        'can_reboot': machine.info['can_reboot'],
        'uuid': machine.info['uuid'],
        'can_destroy': machine.info['can_destroy'],
        'extra': machine.info['extra'],
        'name': machine.info['name'],
        'missing_since': machine.info['missing_since'],
        'tags': machine.info['tags'],
        'can_stop': machine.info['can_stop'],
        'private_ips': machine.info['private_ips'],
        'imageId': machine.info['imageId'],
        'public_ips': machine.info['public_ips'],
        'state': machine.info['state'],
        'can_suspend': machine.info['can_suspend'],
        'can_rename': machine.info['can_rename'],
        'can_undefine': machine.info['can_undefine'],
        'can_tag': machine.info['can_tag'],
        'last_seen': machine.info['last_seen'],
        'id': machine.info['id'],
        'can_resume': machine.info['can_resume'],
        'size': machine.info['size']
    },
    'mist_type': 'machine',
    'machine_id': machine.info['id'],
    'ip': machine.info['public_ips'][0],
    'master_ip': ctx.instance.runtime_properties['master_ip'],
    'networks:': [machine.info['public_ips'][0]]
}
node_instance['relationships'] = [
    {
        'target_id': ctx.instance.id,
        'target_name': 'kube_master',
        'type': 'cloudify.relationships.connected_to'
    }
]

_storage = ('../local-storage/local/node-instances')
_instance_file = open(os.path.join(_storage, node_instance['id']), 'w')
_instance_file.write(json.dumps(node_instance))
_instance_file.close()
