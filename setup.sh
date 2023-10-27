#!/bin/bash

GREEN=`tput setaf 2 bold`
RED=`tput setaf 1 bold`
RESET=`tput sgr0`

command_exists() {
  if command -v "$1" &>/dev/null; then
    echo "$GREEN[+] Command '$1' is available at $(command -v "$1")$RESET"
    return 1
  else
    echo "$RED[x] Command '$1' does not exist, install $1 to continue$RESET"
    return 0
  fi
}

get_os() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "linux"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macos"
  elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo "cygwin"
  elif [[ "$OSTYPE" == "msys" ]]; then
    echo "windows"
  elif [[ "$OSTYPE" == "win32" ]]; then
    echo "windows"
  elif [[ "$OSTYPE" == "freebsd"* ]]; then
    echo "freebsd"
  else
    echo "unknown"
  fi
}

$is_pip = 0
$is_pip3 = 0
$is_pipx = 0

# Check if required dependencies exist
command_exists git
command_exists poetry
command_exists docker

if [[ $(get_os) != "linux" ]]; then
  command_exists pip
  is_pip=$?
  command_exists pip3
  is_pip3=$?
else
  command_exists pipx
  is_pipx=$?
fi


git_path=$(command -v git)
poetry_path=$(command -v poetry)
docker_path=$(command -v docker)
os=$(get_os)

$git_path clone https://github.com/abhirambsn/kali-docker.git $HOME/kali-docker
cd kali-docker/kalictl
$poetry_path install # Install script and dependencies
$poetry_path build # Build Dependencies

echo "OS -> $os"
if [[ $os -ne "linux" ]]; then
  if $is_pip; then
    $(command -v pip) install dist/*.whl
  elif $is_pip3; then
    $(command -v pip3) install dist/*.whl
  else
    echo "$RED[x] pip or pip3 not found, install either of them to continue$RESET"
    exit 1
  fi
else
  if $is_pipx; then
    $(command -v pipx) install dist/*.whl
  else
    echo "$RED[x] pipx not found, install it to continue$RESET"
    exit 1
  fi
fi

kalictl_path=$(command -v kalictl)

# Create a docker network with name kali-net and subnet 10.0.0.0/16
$docker_path network create kali-net --subnet=10.0.0.0/16


kalictl init # Initialize config
kalictl build # Build Images
kalictl start # Start the compose stack

echo "[+] Execute 'kalictl exec /bin/bash' to enter the container's shell"
echo "For more usage information, use 'kalictl [<command>] --help'"
