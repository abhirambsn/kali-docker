#!/bin/bash

command_exists() {
  if command -v "$1" &>/dev/null; then
    echo "Command '$1' exists"
  else
    echo "Command '$1' does not exist, install $1 to continue"
    exit 1
  fi
}

# Check if required dependencies exist
command_exists git
command_exists poetry
command_exists docker

git_path=$(command -v git)
poetry_path=$(command -v poetry)

$git_path clone https://github.com/abhirambsn/kali-docker.git
cd kali-docker/kalictl
$poetry_path install # Install script and dependencies

kalictl_path=$(command -v kalictl)

# Create a docker network with name kali-net and subnet 10.0.0.0/16
$docker_path network create kali-net --subnet=10.0.0.0/16

$kalictl_path init # Initialize config
$kalictl_path build # Build Images
$kalictl_path start # Start the compose stack

echo "[+] Execute 'kalictl exec /bin/bash' to enter the container's shell"
echo "For more usage information, use 'kalictl [<command>] --help'"
