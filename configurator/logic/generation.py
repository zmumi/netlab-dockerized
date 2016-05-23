# -*- coding: utf-8 -*-
import ipaddress
import os
import zipfile


def run(nodes, edges, template_loader, dir="."):
    params = data_as_context(edges, nodes)
    _clean_dir(dir)

    _render('design.json', {'nodes': nodes, 'edges': edges}, dir + '/design.json', template_loader)
    _render('docker-compose.yml', params, dir + '/docker-compose.yml', template_loader)
    _render('up.sh', params, dir + '/up.sh', template_loader)
    _render('Dockerfile', params, dir + '/Dockerfile', template_loader)

    for (router, router_params) in params['routers'].items():
        _render('config.boot', router_params, dir + '/' + router + '-config.boot', template_loader)

    _zip_project(dir)


def _zip_project(dir):
    for root, dirs, files in os.walk(dir):
        with zipfile.ZipFile(dir + "/project.zip", "w", zipfile.ZIP_DEFLATED) as ziph:
            for file in [f for f in files if f != "project.zip" and not f.endswith(".template")]:
                ziph.write(os.path.join(root, file))


def _clean_dir(dir):
    for f in [dir + '/' + f for f in os.listdir(dir) if f.endswith(".boot")]:
        os.remove(f)


def data_as_context(edges, nodes):
    params = {
        'clients': {},
        'routers': {},
        'networks': {},
    }
    for node in nodes:
        properties = node['properties']
        if properties['type'] == 'router':
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
        if properties['type'] == 'client':
            client_id = edge['from']
            network_id = edge['to']
            client_ip = properties['ip']
            client_gateway = properties['gateway']
            params['clients'][client_id] = {
                'network': network_id,
                'ip': client_ip,
                'gateway': client_gateway
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
