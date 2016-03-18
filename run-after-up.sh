#!/bin/bash

docker exec -it zaawtechintsys_router1_1 cp  /injected/router1-config.boot  /config/config.boot
docker exec -it zaawtechintsys_router2_1 cp  /injected/router2-config.boot  /config/config.boot
docker exec -it zaawtechintsys_router1_1 /etc/init.d/vyatta-router restart
docker exec -it zaawtechintsys_router2_1 /etc/init.d/vyatta-router restart