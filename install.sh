#!/bin/bash

if [ "$(whoami)" != "root" ]; then
	echo "Need root to install"
	exit 255
fi

mkdir -p /opt/serial-bridge/
cp bridge.py /opt/serial-bridge/
cp bridge.service /etc/systemd/system/
chmod 664 /etc/systemd/system/bridge.service

systemctl daemon-reload
systemctl enable bridge
systemctl start bridge
systemctl status bridge
