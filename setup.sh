#!/bin/bash
apt-get update
apt-get install python3-dev libjpeg-dev zlib1g-dev pigpio portaudio19-dev
systemctl enable --now pigpiod
sudo raspi-config nonint do_i2c 0