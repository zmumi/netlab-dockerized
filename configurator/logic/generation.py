# -*- coding: utf-8 -*-
import ipaddress


def run(nodes, edges, template_loader, dir="."):
    params = data_as_context(edges, nodes)

    print params
    print nodes
    print edges

    _render('design.json', {'nodes': nodes, 'edges': edges}, dir + '/design.json', template_loader)
    _render('docker-compose.yml', params, dir + '/docker-compose.yml', template_loader)
    _render('up.sh', params, dir + '/up.sh', template_loader)

    for (router, router_params) in params['routers'].items():
        _render('config.boot', router_params, dir + '/' + router + '-config.boot', template_loader)


def data_as_context(edges, nodes):
    params = {
        'clients': {},
        'routers': {},
        'networks': {},
    }
    for node in nodes:
        properties = node['properties']
        if properties['type'] == 'client':
            params['clients'][node['id']] = {
                'network': properties['network'],
                'ip': properties['ip'],
                'gateway': properties['gateway'],
            }
        elif properties['type'] == 'router':
            params['routers'][node['id']] = {
                'networks': {}
            }
        elif properties['type'] == 'lan':
            net = properties['subnet']
            parsed = ipaddress.ip_network(net)
            reserved = parsed.hosts().next()
            params['networks'][node['id']] = {
                'subnet': net,
                'docker_gateway': reserved
            }
    for edge in edges:
        properties = edge['properties']
        if properties['type'] == 'router':
            lan = edge['to']
            subnet = params['networks'][lan]['subnet']
            parsed = ipaddress.ip_network(subnet)
            params['routers'][edge['from']]['networks'][lan] = {
                'ipv4': properties['ip'],
                'mac': predict_mac_address(properties),
                'mask': str(parsed.prefixlen)
            }

    return params


# predicts mac address according to current implementation:
# https://github.com/docker/docker/blob/3d13fddd2bc4d679f0eaa68b0be877e5a816ad53/vendor/src/github.com/docker/libnetwork/netutils/utils.go#L104
# such hack enables us to properly identify interfaces later on (what enables us to configure them)
def predict_mac_address(properties):
    return "02:42:" + ":".join(map(lambda x: "%.2x" % int(x), properties['ip'].split(".")))


def _render(template, params, path, template_loader):
    with open(path, 'w') as output_file:
        output_file.write(template_loader.render_to_string(template, params))
