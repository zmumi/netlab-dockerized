# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('templating', 'templates'))

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
                    'ipv4': '10.1.0.101'
                },
                'lan8': {
                    'ipv4': '8.1.0.101'
                },
                'lan7': {
                    'ipv4': '7.1.0.101'
                }
            }
        },
        'router-2': {
            'networks': {
                'lan9': {
                    'ipv4': '9.1.0.102'
                },
                'lan8': {
                    'ipv4': '8.1.0.102'
                },
                'lan7': {
                    'ipv4': '7.1.0.102'
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

compose_template = env.get_template('docker-compose.yml')
compose_template.stream(params).dump('docker-compose.yml')
print compose_template.render(params)

up_template = env.get_template('up.sh')
up_template.stream(params).dump('up.sh')
print up_template.render(params)
