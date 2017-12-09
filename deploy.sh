#!/bin/bash
docker stack deploy --compose-file=<(docker-compose -f docker-compose.infra.yml -f docker-compose.yml config 2>/dev/null) $1
