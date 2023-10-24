#!/usr/bin/env bash

ROOT_PATH=$HOME/Security/kali-docker

os_name=$(uname)
user=$1

if [ $# -ne 1 ]; then
  echo "Usage $0 <username>"
  exit 1
fi

# Run Docker Desktop Script in case of Mac or Windows
# Else run Docke Engine Script

docker_desktop_script=$ROOT_PATH/launch_kali_docker_desktop.sh
docker_engine_script=$ROOT_PATH/launch_kali_docker_engine.sh

if [[ $(uname -s) == Linux* ]]; then
  $docker_engine_script $1
else
  $docker_desktop_script $1
fi
