#!/bin/bash
pip install -r requirements.txt
sudo apt-get -y update
sudo apt-get -y upgrade

# Need to install the not Snap version of Chroem
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Dependencies are all kinds of borked, install them
sudo apt-get -y install -f
rm google-chrome-stable_current_amd64.deb

# Selenium webdriver, watch the version, this is fragile
wget https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/chromedriver
rm chromedriver_linux64.zip
