# microservices

## Useful actions
Kill all runned containers:
`docker kill $(docker ps -q)`

### Working with VM
For create virtual machine using Google Compute Engine driver use following command:
`docker-machine create --driver google --google-project {{ project-id }} --google-zone europe-west1-b --google-machine-type f1-micro --google-machine-image $(gcloud compute images list --filter ubuntu-1604-lts --uri) {{ machine-name }}`, replace placeholders to your own.

For remove created VM use:
`docker-machine rm {{ machine-name }}`

Check the state of created machines:
`docker-machine ls`

__Don't forget__ to set environment variables through command:
`eval $(docker-machine env {{ machine-name }})`

For properly work of app incoming trafic for 9292 port should be allowed. For GCE do this through the command:
`gcloud compute firewall-rules create reddit-app --allow tcp:9292 --priority=65534 --target-tags=docker-machine --description="Allow TCP connections" --direction=INGRESS`

## Monolith
Monolith directory contains files for building docker image based on ubuntu:16.04 with installed mongod, ruby, bundle and deployed [reddit app](https://github.com/Artemmkin/reddit)

## Microservices architecture
[Reddit app](https://github.com/Artemmkin/reddit/tree/microservices) divided on services.

Build images:
`docker build -t <your-login>/post:1.0 ./post-py`
`docker build -t <your-login>/comment:1.0 ./comment`
`docker build -t <your-login>/ui:1.0 ./ui`

To connect containers into network it should be created before:
`docker network create backend --subnet=10.0.2.0/24`
`docker network create frontend --subnet=10.0.1.0/24`

Create volume to store db data:
`docker volume create reddit_db`

Before run containers pull the latest mongod image:
`docker pull mongo:latest`

Run containers:
`docker run -d --name=mongo_db --net=backend --net-alias=post_db --net-alias=comment_db -v reddit_db:/data/db mongo:latest`
`docker run -d --name=post --net=backend <your-login>/post:1.0`
`docker run -d --name=comment --net=backend <your-login>/comment:1.0`
`docker run -d --name=ui --net=frontend -p 9292:9292 <your-login>/ui:1.0`

After containers was runned connect them to existing networks:
`docker network connect frontend post`
`docker network connect frontend comment` 

 backend
+--------------------------------+
|                                |    frontend
|  mongo_db  +--------------------------------+
|            |                   |            |
|            |   comment   post  |    ui      |
+--------------------------------+            |
             |                                |
             +--------------------------------+
