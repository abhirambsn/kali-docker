#!/bin/bash

user=$1
ssh_path=$(which ssh)

echo "Executing $ssh_path $1@10.0.0.2"
$ssh_path $1@10.0.0.2 
