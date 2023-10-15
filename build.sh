docker build -t kali-custom --build-arg gid=$(id -g) --build-arg uid=$(id -u) --build-arg user=$1 --build-arg group=$1 .
