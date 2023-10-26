# Kali Docker

Kali Linux to run on any OS in a Docker Container

## Setup Instructions

Follow the below instructions on your terminal to get setup with the tool.

or you can use our readymade `setup.sh` script for the same

### Automated Script
```bash
curl https://raw.githubusercontent.com/abhirambsn/kali-docker/main/setup.sh | bash
```

### Manual Way

#### Pre-requisites
1. Docker
2. Docker Compose
3. Poetry
4. Git

#### Clone the Repository
```bash
git clone https://github.com/abhirambsn/kali-docker.git
```

#### Install Script and Dependencies using poetry

*Install poetry before executing this section*

```bash
cd kali-docker/kalictl
poetry install
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