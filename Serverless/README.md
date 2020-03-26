# AWS SAM cli on Ubuntu

## Instructions

1) run following command to update OS
```
sudo apt-get update
```

2) run following command to remove docker if its already installed
```
sudo apt-get remove docker docker-engine docker.io
```

3) run following command to install docker 
```
sudo apt install docker.io
```
4) Run following command to start docker
```
sudo systemctl start docker
```
5) Run following command to make sure docker runs at startup
```
sudo systemctl enable docker
```
6) Run following command to run docker without sudo.
```
sudo usermod -a -G docker ubuntu
```
7) Log off and log in again and Run following command to see if docker is installed
```
docker ps
```
8) Install git if its not installed already. git is needed to install homebrew/linuxbrew later.
```
sudo apt-get install git
```
9) Install Homebrew/linuxbrew
```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
```
10) Next, add Homebrew to your PATH by running the following commands. These commands work on all major flavors of Linux by adding either ~/.profile on Debian/Ubuntu or ~/.bash_profile on CentOS/Fedora/RedHat:
```
test -d ~/.linuxbrew && eval $(~/.linuxbrew/bin/brew shellenv)
test -d /home/linuxbrew/.linuxbrew && eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile
echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile
```
11) Run following command to verify if linuxbrew got installed
```
brew --version
```

12) Install AWS SAM CLI using following commands
```
brew tap aws/tap
brew install aws-sam-cli
```
Note: If you get error while it installing patchelf, run follwoing to install essential and then the above command again.
```
sudo apt-get install build-essential
```

13) Run following command to verify if SAM got installed
```
sam --version
```
