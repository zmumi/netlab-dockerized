#!/bin/bash

./docker-compose up -d
sleep 5

{% for router_name, params in routers.items() %}
#############################
###### {{router_name}} ######
#############################

docker exec -it {{router_name}} cp  /injected/{{router_name}}-config.boot  /config/config.boot
{% for lan_name, lan_params in params['networks'].items() %}
INTERFACE_NAME=`docker exec -it {{router_name}} ifconfig | grep -B1 "HWaddr {{lan_params['mac']}}"  | awk '{print $1}' | xargs`
docker exec -it {{router_name}} sed -i.bak s/PLACEHOLDER_{{lan_params['mac']}}/$INTERFACE_NAME/g /config/config.boot
{% endfor %}
docker exec -it {{router_name}} /etc/init.d/vyatta-router restart
{% endfor %}
