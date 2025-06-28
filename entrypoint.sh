#!/bin/bash

# Start Apache in background
apachectl -D FOREGROUND &

# Wait for server to become available
echo "Waiting for Apache to start..."
sleep 5

# Run your test file
python3 -m unittest -v tests/test_taskmanager.py
