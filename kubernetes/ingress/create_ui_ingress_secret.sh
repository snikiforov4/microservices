#!/bin/bash

TLS_CRT=`cat tls.crt | base64`
TLS_KEY=`cat tls.key | base64`

eval "echo \"$(cat ui-ingress-secret.yml.template)\"">ui-ingress-secret.yml
