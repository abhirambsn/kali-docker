#!/usr/bin/env bash

user=$1
wd=/home/$1

docker_path=$(which docker)

$docker_path compose exec -u $user -w $wd kali /usr/bin/zsh
