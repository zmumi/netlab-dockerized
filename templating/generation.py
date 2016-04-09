# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader
import ipaddress

env = Environment(loader=PackageLoader('templating', 'templates'))
edges = [{u'to': u'lan10', u'from': u'client-1', u'id': u'client-1/lan10',
          u'properties': {u'ip': u'10.1.0.44', u'type': u'client', u'gateway': u'10.1.0.101'}},
         {u'to': u'lan9', u'from': u'client-2', u'id': u'client-2/lan10',
          u'properties': {u'ip': u'9.1.0.44', u'type': u'client', u'gateway': u'9.1.0.102'}},
         {u'to': u'lan10', u'from': u'router-1', u'id': u'router-1/lan10',
          u'properties': {u'ip': u'10.1.0.101', u'type': u'router'}},
         {u'to': u'lan8', u'from': u'router-1', u'id': u'router-1/lan8',
          u'properties': {u'ip': u'8.1.0.101', u'type': u'router'}},
         {u'to': u'lan7', u'from': u'router-1', u'id': u'router-1/lan7',
          u'properties': {u'ip': u'7.1.0.101', u'type': u'router'}},
         {u'to': u'lan9', u'from': u'router-2', u'id': u'router-2/lan9',
          u'properties': {u'ip': u'9.1.0.102', u'type': u'router'}},
         {u'to': u'lan8', u'from': u'router-2', u'id': u'router-2/lan8',
          u'properties': {u'ip': u'8.1.0.102', u'type': u'router'}},
         {u'to': u'lan7', u'from': u'router-2', u'id': u'router-2/lan7',
          u'properties': {u'ip': u'7.1.0.102', u'type': u'router'}}]
nodes = [{u'color': u'lightgray',
          u'properties': {u'ip': u'10.1.0.44', u'type': u'client', u'network': u'lan10', u'gateway': u'10.1.0.101'},
          u'id': u'client-1', u'label': u'client-1'},
         {u'color': u'lightgray',
          u'properties': {u'ip': u'9.1.0.44', u'type': u'client', u'network': u'lan9', u'gateway': u'9.1.0.102'},
          u'id': u'client-2', u'label': u'client-2'},
         {u'properties': {u'type': u'router'}, u'id': u'router-1', u'label': u'router-1'},
         {u'properties': {u'type': u'router'}, u'id': u'router-2', u'label': u'router-2'},
         {u'color': u'white', u'properties': {u'subnet': u'10.1.0.0/16', u'type': u'lan'}, u'id': u'lan10',
          u'label': u'lan10'},
         {u'color': u'white', u'properties': {u'subnet': u'9.1.0.0/16', u'type': u'lan'}, u'id': u'lan9',
          u'label': u'lan9'},
         {u'color': u'white', u'properties': {u'subnet': u'8.1.0.0/16', u'type': u'lan'}, u'id': u'lan8',
          u'label': u'lan8'},
         {u'color': u'white', u'properties': {u'subnet': u'7.1.0.0/16', u'type': u'lan'}, u'id': u'lan7',
          u'label': u'lan7'}]

gen_params = {
    'clients': {},
    'routers': {},
    'networks': {},
}

for node in nodes:
    properties = node['properties']
    if properties['type'] == 'client':
        gen_params['clients'][node['id']] = {
            'network': properties['network'],
            'ip': properties['ip'],
            'gateway': properties['gateway'],
        }
    elif properties['type'] == 'router':
        gen_params['routers'][node['id']] = {
            'networks': {}
        }
    elif properties['type'] == 'lan':
        net = properties['subnet']
        parsed = ipaddress.ip_network(net)
        reserved = parsed.hosts().next()
        gen_params['networks'][node['id']] = {
            'subnet': net,
            'docker_gateway': reserved
        }

for edge in edges:
    properties = edge['properties']
    if properties['type'] == 'router':
        lan = edge['to']
        subnet = gen_params['networks'][lan]['subnet']
        parsed = ipaddress.ip_network(subnet)
        print lan, subnet
        gen_params['routers'][edge['from']]['networks'][lan] = {
            'ipv4': properties['ip'],
            'mask': str(parsed.prefixlen)
        }

params = {
    'clients': {
        'client-1': {
            'network': 'lan10',
            'ip': '10.1.0.44',
            'gateway': '10.1.0.101'
        },
        'client-2': {
            'network': 'lan9',
            'ip': '9.1.0.44',
            'gateway': '9.1.0.102'
        }
    },
    'routers': {
        'router-1': {
            'networks': {
                'lan10': {
                    'ipv4': '10.1.0.101',
                    'mask': '16'
                },
                'lan8': {
                    'ipv4': '8.1.0.101',
                    'mask': '16'
                },
                'lan7': {
                    'ipv4': '7.1.0.101',
                    'mask': '16'
                }
            }
        },
        'router-2': {
            'networks': {
                'lan9': {
                    'ipv4': '9.1.0.102',
                    'mask': '16'
                },
                'lan8': {
                    'ipv4': '8.1.0.102',
                    'mask': '16'
                },
                'lan7': {
                    'ipv4': '7.1.0.102',
                    'mask': '16'
                }
            }
        }
    },
    'networks': {
        'lan10': {
            'subnet': '10.1.0.0/16',
            'docker_gateway': '10.1.0.254'
        },
        'lan9': {
            'subnet': '9.1.0.0/16',
            'docker_gateway': '9.1.0.254'
        },
        'lan8': {
            'subnet': '8.1.0.0/16',
            'docker_gateway': '8.1.0.254'
        },
        'lan7': {
            'subnet': '7.1.0.0/16',
            'docker_gateway': '7.1.0.254'
        }
    }
}

params = gen_params
compose_template = env.get_template('jinja2/docker-compose.yml')
compose_template.stream(params).dump('docker-compose.yml')
print compose_template.render(params)

up_template = env.get_template('jinja2/up.sh')
up_template.stream(params).dump('up.sh')
print up_template.render(params)

for (router, router_params) in params['routers'].items():
    up_template = env.get_template('jinja2/config.boot')
    up_template.stream(router_params).dump(router + '-config.boot')
    print up_template.render(router_params)
