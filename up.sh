#!/bin/bash

docker-compose up -d
sleep 5

docker exec -it zaawtechintsys_router1_1 cp  /injected/router1-config.boot  /config/config.boot
docker exec -it zaawtechintsys_router2_1 cp  /injected/router2-config.boot  /config/config.boot
docker exec -it zaawtechintsys_router1_1 /etc/init.d/vyatta-router restart
docker exec -it zaawtechintsys_router2_1 /etc/init.d/vyatta-router restart

docker exec -it zaawtechintsys_client1_1 ping 9.1.0.44
