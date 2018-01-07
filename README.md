# microservices

### Useful commands
Kill all runned containers:
`docker kill $(docker ps -q)`

### Working with VM
For create virtual machine using Google Compute Engine driver use following command:
`docker-machine create --driver google --google-project {{ project-id }} --google-zone europe-west1-b --google-machine-type f1-micro --google-machine-image $(gcloud compute images list --filter ubuntu-1604-lts --uri) {{ machine-name }}`, replace placeholders to your own.

For remove VM use:
`docker-machine rm {{ machine-name }}`

Check the state of created machines:
`docker-machine ls`

Show ip of a created VM:
`docker-machine ip {{ machine-name }}`

__Don't forget__ to set environment variables through command:
`eval $(docker-machine env {{ machine-name }})`

For properly work of app incoming trafic for 9292 port should be allowed. For GCE do this through the command:
`gcloud compute firewall-rules create reddit-app --allow tcp:9292 --priority=65534 --target-tags=docker-machine --description="Allow TCP connections" --direction=INGRESS`

## Monolith
Monolith directory contains files for building docker image based on ubuntu:16.04 with installed mongod, ruby, bundle and deployed [reddit app](https://github.com/Artemmkin/reddit)

## Microservices architecture
[Reddit app](https://github.com/Artemmkin/reddit/tree/microservices) divided on services.

Build images:
```
docker build -t <your-login>/post:1.0 ./post-py
docker build -t <your-login>/comment:1.0 ./comment
docker build -t <your-login>/ui:1.0 ./ui
```

To connect containers into network it should be created before:
```
docker network create backend --subnet=10.0.2.0/24
docker network create frontend --subnet=10.0.1.0/24
```

Create volume to store db data:
`docker volume create reddit_db`

Before run containers pull the latest mongod image:
`docker pull mongo:latest`

Run containers:
```
docker run -d --name=mongo_db --net=backend --net-alias=post_db \
--net-alias=comment_db -v reddit_db:/data/db mongo:latest
docker run -d --name=post --net=backend <your-login>/post:1.0
docker run -d --name=comment --net=backend <your-login>/comment:1.0
docker run -d --name=ui --net=frontend -p 9292:9292 <your-login>/ui:1.0
```

After containers was runned connect them to existing networks:
```
docker network connect frontend post
docker network connect frontend comment
``` 

```
 backend
+--------------------------------+
|                                |    frontend
|  mongo_db  +--------------------------------+
|            |                   |            |
|            |   comment   post  |    ui      |
+--------------------------------+            |
             |                                |
             +--------------------------------+
```

## Docker compose
[Documentaion](https://docs.docker.com/compose/overview/)

[Compose CLI](https://docs.docker.com/compose/reference/overview/#command-options-overview-and-help)

__Useful commands__:

Create and start containers: `docker-compose up -d`

Stop and remove containers, networks, images, and volumes: `docker-compose down`

List containers: `docker-compose ps`

For correct work of Compose define your own [default environment file](https://docs.docker.com/compose/env-file/) **.env**.
Example of such file **.env.example** placed in the root of repo and contains all needed variables.
To check yourself use the command: `docker-compose config`

## Working with Monitoring

For properly work of your application __allow__ traffic for the following ports:

```
== Prometheus ==
gcloud compute firewall-rules create prometheus-default --allow tcp:9090

== HTTP incoming traffic ==
gcloud compute instances add-tags {{ vmname }} --tags http-server

== cAdvisor ==
gcloud compute firewall-rules create cadvisor-default --allow tcp:8080

== Grafana ==
gcloud compute firewall-rules create grafana-default --allow tcp:3000
```

To run prometheus in container use the following command:
`docker run --rm -p 9090:9090 -d --name prometheus prom/prometheus`

## Swarm mode
How to create swarm and use swarm mode could be found [this](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/) tutorial

How to join nodes to cluster [here](https://docs.docker.com/engine/swarm/join-nodes/#join-as-a-worker-node)

__Keep in mind__ that all docker stack and docker service commands must be run from a manager node.
To distribute the images across the swarm, it needs to be __pushed to the registry__.

Bring the registry down with: `docker service rm`

Put the label `prometheus` for one of the nodes for witch you want to deploy prometheus and alertmanager services: 
`docker node update --label-add prometheus=true <node-name>`

To deploy application use the script `deploy.sh` for example: `./deploy.sh ENV`. ENV is required to correct work.

### Working with multiple environments
`switch.py` allow you to replace all properties in `.env` to right ones specified for choosen environment.
Each property file has naming scheme: `(default|ENV_NAME).env`

To run to new environment use the following command: `switch.py -e ENV_NAME`

`default.env` contains properties shared for all environments and also props for __default__ environment. If -e ENV_NAME isn't specified default.env will be used.

To deploy env use the following command: `deploy.py -e ENV_NAME`. If -e ENV_NAME isn't specified the script will try to get ENV_NAME from .env file ENV variable else error will occur.

## Kubernetes


### TLS
Use openssl to generate key and certificate: `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN={{ IP_OR_DOMAIN }}"`. To get ip use the following command: `kubectl get ingress/ui -n dev`.

Replace variables in `ui-ingress-secret.yml.template` manualy or by running the script: `create_ui_ingress_secret.sh`(tls.key and tls.crt shoul be inside `ingress` directory). Generated `ui-ingress-secret.yml` file could be used to to create secret in k8s.
