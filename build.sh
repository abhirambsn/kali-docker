docker build -t kali-custom --build-arg gid=$(id -g) --build-arg uid=$(id -u) --build-arg user=abhiram-bhallamudi --build-arg group=abhiram-bhallamudi .
