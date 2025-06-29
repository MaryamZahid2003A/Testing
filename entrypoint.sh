#!/bin/bash

# Start Apache in the background
apachectl -D FOREGROUND &

# Wait a few seconds to ensure Apache is up
sleep 5

# Run Selenium tests
python3 -m unittest -v tests/test_taskmanager.py
