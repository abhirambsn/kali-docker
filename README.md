# Kali Docker

Kali Linux to run on any OS in a Docker Container

## Setup Instructions

Follow the below instructions on your terminal to get setup with the tool.

or you can use our readymade `setup.sh` script for the same

### Pre-requisites
Ensure that the following are installed before proceeding with any of the installation methods:

1. Docker Engine or Docker Desktop (WSL2 Backend required for Windows Hosts)
2. Docker Compose
3. Python
4. Poetry
5. Git

### Automated Script
```bash
curl https://raw.githubusercontent.com/abhirambsn/kali-docker/main/setup.sh | bash
```

### Manual Way

#### Clone the Repository
```bash
git clone https://github.com/abhirambsn/kali-docker.git
```

#### Install Script and Dependencies using poetry & pip

*Install poetry before executing this section*

```bash
cd kali-docker/kalictl
poetry install
poetry build
pip3 install dist/*.whl
```

#### Create a Docker Network with name kali-net and subnet 10.0.0.0/16

```bash
docker network create kali-net --subnet=10.0.0.0/16
```

#### Use the installed kalictl to initialize, build and start the containers

```bash
kalictl init # Initialize config
kalictl build # Build Images
kalictl start # Start the compose stack
kalictl exec /bin/bash # To Get into shell
```