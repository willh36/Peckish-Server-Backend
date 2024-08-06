#!/bin/bash

# Install Python
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Install Python packages
python3 -m pip install -r requirements.txt