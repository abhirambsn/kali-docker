#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <username> <password>"
    exit 1
fi

os_name=$(uname)

echo "Building on $os_name host"
# Check if OS is mac then ask for uid and gid
gid=0
uid=0

if [ $os_name == "Darwin" ]; then
  gid=1000
  uid=1000
elif [ "$(expr substr $os_name 1 5)" == "Linux" ]; then
  gid=$(id -g)
  uid=$(id -u)
else
  gid=1000
  uid=1000
fi

echo "Using GID: $gid and UID: $uid"

docker_path=$(which docker)

$docker_path build -f docker/Dockerfile.kali -t abhirambsn/kali-custom --build-arg gid=$gid --build-arg uid=$uid --build-arg user=$1 --build-arg group=$1 .
$docker_path build -f docker/Dockerfile.kracking -t abhirambsn/kracking .
$docker_path build -f docker/Dockerfile.penbuntu -t abhirambsn/penbuntu --build-arg user=$1 .
