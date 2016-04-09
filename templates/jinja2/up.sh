#!/bin/bash

../docker-compose up -d
sleep 5

{% for router_name, params in routers.items() %}
docker exec -it {{router_name}} cp  /injected/{{router_name}}-config.boot  /config/config.boot
docker exec -it {{router_name}} /etc/init.d/vyatta-router restart
{% endfor %}
