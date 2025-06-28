#!/bin/bash

# Start Apache in background
apachectl -D FOREGROUND &

# Wait for it to come up
sleep 5

# Run tests
python3 -m unittest -v tests/test_taskmanager.py
