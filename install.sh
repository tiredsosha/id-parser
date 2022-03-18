#!/bin/bash
sudo apt update  
sudo apt install software-properties-common  
sudo add-apt-repository ppa:deadsnakes/ppa  
sudo apt install python3.8
sudo apt install python3.7  
sudo apt update
sudo apt install python3-pip
python3.8 -m pip install asyncio-mqtt
python3.8 -m pip install pyaml
python3.8 -m pip install pydantic
python3.7 -m pip install asyncio-mqtt
python3.7 -m pip install pyaml
python3.7 -m pip install pydantic

sudo chmod +x main.py
sudo touch /lib/systemd/system/parser.service
sudo tee -a /lib/systemd/system/parser.service <<EOF
[Unit]
Description=Park ID parser
After=multi-user.target
[Service]
Type=simple
User=$1
WorkingDirectory=/home/$1/hc-id-parser
ExecStart=/home/$1/hc-id-parser/main.py
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload 
sudo systemctl enable parser.service 
sudo systemctl start parser.service
# sudo reboot
