# microservices

Build docker image based on ubuntu:16.04 with installed mongod, ruby, bundle and deployed [reddit app](https://github.com/Artemmkin/reddit.git)

For create virtual machine using Google Compute Engine driver use following command:
`docker-machine create --driver google --google-project {{ project-id }} --google-zone europe-west1-b --google-machine-type f1-micro --google-machine-image $(gcloud compute images list --filter ubuntu-1604-lts --uri) {{ machine-name }}`, replace placeholders to your own.

Check the state of created machines:
`docker-machine ls`

Don't forget to set environment variables through command:
`eval $(docker-machine env {{ machine-name }})`

For properly work of app you should allow incoming trafic for 9292 port. For GCE do this through the command:
`gcloud compute firewall-rules create reddit-app --allow tcp:9292 --priority=65534 --target-tags=docker-machine --description="Allow TCP connections" --direction=INGRESS`
