# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('templating', 'templates'))

params = {
    'clients': {
        'client-hostname-1': {
            'network': 'lan10',
            'ip': '10.1.0.44',
            'gateway': '10.1.0.101',
            'ping': '9.1.0.44',
        },
        'client-hostname-2': {
            'network': 'lan9',
            'ip': '9.1.0.44',
            'gateway': '9.1.0.102',
            'ping': '10.1.0.44',

        }
    }
}

template = env.get_template('docker-compose.yml')
template.stream(params).dump('docker-compose.yml')

print template.render(params)
