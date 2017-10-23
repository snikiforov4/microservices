# microservices

## Useful actions 
Kill all runned containers:
`docker kill $(docker ps -q)`

## Monolith
Monolith directory contains files for build docker image based on ubuntu:16.04 with installed mongod, ruby, bundle and deployed [reddit app](https://github.com/Artemmkin/reddit.git)

For create virtual machine using Google Compute Engine driver use following command:
`docker-machine create --driver google --google-project {{ project-id }} --google-zone europe-west1-b --google-machine-type f1-micro --google-machine-image $(gcloud compute images list --filter ubuntu-1604-lts --uri) {{ machine-name }}`, replace placeholders to your own.

Check the state of created machines:
`docker-machine ls`

Don't forget to set environment variables through command:
`eval $(docker-machine env {{ machine-name }})`

For properly work of app you should allow incoming trafic for 9292 port. For GCE do this through the command:
`gcloud compute firewall-rules create reddit-app --allow tcp:9292 --priority=65534 --target-tags=docker-machine --description="Allow TCP connections" --direction=INGRESS`

## Microservices architecture
Pull latest mongod image before run it:
`docker pull mongo:latest`

Build images:
`docker build -t <your-login>/post:1.0 ./post-py`
`docker build -t <your-login>/comment:1.0 ./comment`
`docker build -t <your-login>/ui:1.0 ./ui`

Connect containers into network it should be created before:
`docker network create reddit`

Create volume to store db data:
`docker volume create reddit_db`

Run containers:
`docker run -d --net=reddit -v reddit_db:/data/db --net-alias=post_db --net-alias=comment_db mongo:latest`
`docker run -d --net=reddit --net-alias=post <your-login>/post:1.0`
`docker run -d --net=reddit --net-alias=comment <your-login>/comment:1.0`
`docker run -d --net=reddit -p 9292:9292 <your-login>/ui:1.0`
