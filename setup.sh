#!/bin/bash

mkdir -p .keys
cp_path=$(which cp)
cp ~/.ssh/id_rsa* .keys
