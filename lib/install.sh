#!/usr/bin/env bash

# https://developers.supportbee.com/blog/setting-up-cucumber-to-run-with-Chrome-on-Linux/
# https://gist.github.com/curtismcmullan/7be1a8c1c841a9d8db2c
# http://stackoverflow.com/questions/10792403/how-do-i-get-chrome-working-with-selenium-using-php-webdriver
# http://stackoverflow.com/questions/26133486/how-to-specify-binary-path-for-remote-chromedriver-in-codeception
# http://stackoverflow.com/questions/40262682/how-to-run-selenium-3-x-with-chrome-driver-through-terminal
# http://askubuntu.com/questions/760085/how-do-you-install-google-chrome-on-ubuntu-16-04

# Versions
CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`

# Remove existing downloads and binaries so we can start from scratch.
sudo apt-get remove -y google-chrome-stable
rm ~/chromedriver_linux64.zip
sudo rm /usr/local/bin/chromedriver

# Install dependencies.
sudo apt-get update
sudo apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4

# Install Chrome.
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable

# Install ChromeDriver.
cd ~
wget https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip 
unzip chromedriver_linux64.zip  
rm chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver

# Install required libraries for python2
sudo apt-get install python-pip
pip install selenium future requests 

# Install required libraries for python3
sudo apt-get install python3-pip
pip install selenium future requests 
