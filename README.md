# Kali Docker

Kali Linux to run on any OS in a Docker Container

## Setup Instructions

Follow the below instructions on your terminal to get setup with the tool.

or you can use our readymade `setup.sh` script for the same

### Automated Script
```bash
wget https://raw.githubusercontent.com/abhirambsn/setup.sh | bash
```

### Manual Way
```bash
git clone https://github.com/abhirambsn/kali-docker.git
cd kali-docker/kalictl
poetry install # Install script and dependencies

kalictl init # Initialize config
kalictl build # Build Images
kalictl start # Start the compose stack
kalictl exec /bin/bash # To Get into shell
```