#!/bin/bash
# ---------------------------------------------------------

docker build --network=host -t "resnet-server" -f "docker/Dockerfile" . 