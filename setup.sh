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
docker_path=$(command -v docker)

$git_path clone https://github.com/abhirambsn/kali-docker.git $HOME/kali-docker
cd kali-docker/kalictl
$poetry_path install # Install script and dependencies
$poetry_path build # Build Dependencies
$(command -v pip3) install dist/*.whl
kalictl_path=$(command -v kalictl)

# Create a docker network with name kali-net and subnet 10.0.0.0/16
$docker_path network create kali-net --subnet=10.0.0.0/16


kalictl init # Initialize config
kalictl build # Build Images
kalictl start # Start the compose stack

echo "[+] Execute 'kalictl exec /bin/bash' to enter the container's shell"
echo "For more usage information, use 'kalictl [<command>] --help'"
