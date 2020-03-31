
# Docker

## Overview

## Installation Instruction For Amazon Linux EC2

1. Check of os release
```
cat /etc/os-release
```

2. Update yum util and device mapper
```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

3. Add repository (ce - community edition, ee - enterprise edition
```
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

4. Install docker
```
sudo yum install docker-ce
```

5. Enable docker
```
sudo systemctl enable docker
```

6. Start docker
```
sudo systemctl start docker
```

7. Add ec2-user to docker group to avoid sudo for running docker commands further
```
sudo usermod -a -G docker ec2-user
```

8. Run hello-world docker image
```
docker run hello-world
```
