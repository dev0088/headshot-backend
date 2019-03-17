#!/bin/bash

sudo systemctl enable uwsgi
sudo systemctl start uwsgi
sudo systemctl status uwsgi
