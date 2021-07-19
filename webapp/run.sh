#!/usr/bin/env bash

export FLASK_APP=server
pkill -f flask
sleep 1
flask run -h 0.0.0.0 --reload --debugger --extra-files templates/section.html &

sleep 1
firefox-bin "http://localhost:5000"
