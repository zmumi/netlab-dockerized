#!/bin/bash

docker-compose up -d
sleep 10

{% for client_name, params in clients.items() %}
#############################
###### {{client_name}} ######
#############################

docker exec {{client_name}} /bin/bash -c "route del default;route add default gw {{ params['gateway'] }} eth0; route"
{% endfor %}

{% for router_name, params in routers.items() %}
#############################
###### {{router_name}} ######
#############################

docker cp {{router_name}}-config.boot {{router_name}}:/config.boot.template
docker exec {{router_name}} cp  /config.boot.template  /config/config.boot
{% for lan_name, lan_params in params['networks'].items() %}
INTERFACE_NAME=`docker exec {{router_name}} ifconfig | grep -B1 "HWaddr {{lan_params['mac']}}"  | awk '{print $1}' | xargs`
docker exec {{router_name}} sed -i.bak s/PLACEHOLDER_{{lan_params['mac']}}/$INTERFACE_NAME/g /config/config.boot
{% endfor %}
docker exec {{router_name}} /etc/init.d/vyatta-router restart
{% endfor %}

####################################################
###### Fix network problems on docker-machine ######
####################################################

docker-compose restart
sleep 4
{% for router_name, params in routers.items() %}
docker exec {{router_name}} service ssh restart {% endfor %}
{% for client_name, params in clients.items() %}
docker exec {{client_name}} service ssh restart {% endfor %}