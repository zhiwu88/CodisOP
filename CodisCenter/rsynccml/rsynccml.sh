#!/bin/bash
source /etc/profile

scp 10.0.0.1:/home/work/CodisInstaller/tools/ClusterManager/ClusterManager.db .
/usr/bin/python /home/work/CodisCenter/rsynccml/rsynccml.py
