

#Instructions

1) run following command
```
sudo apt-get update
```

```
sudo apt-get remove docker docker-engine docker.io
```

```
sudo apt install docker.io
```

```
sudo systemctl start docker
```

```
sudo systemctl enable docker
```

```
sudo usermod -a -G docker ec2-user
```


```
docker ps
```
Install git
```
sudo apt-get install git
```
Install Homebrew

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
```

```
test -d ~/.linuxbrew && eval $(~/.linuxbrew/bin/brew shellenv)
test -d /home/linuxbrew/.linuxbrew && eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile
echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile
```

```
brew --version
```
```
brew tap aws/tap
```

```
brew install aws-sam-cli
```
Error with patchelf - readelf was not installed. run follwoing

```
sudo apt-get install build-essential
```

Then again run following
```
brew install aws-sam-cli
```

```
sam --version
```







