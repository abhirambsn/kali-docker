#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <username> <password>"
    exit 1
fi

docker_path=$(which docker)

$docker_path build -f docker/Dockerfile.kali -t abhirambsn/kali-custom --build-arg gid=$(id -g) --build-arg uid=$(id -u) --build-arg user=$1 --build-arg group=$1 .
$docker_path build -f docker/Dockerfile.kracking -t abhirambsn/kracking .
$docker_path build -f docker/Dockerfile.penbuntu -t abhirambsn/penbuntu --build-arg user=$1 .