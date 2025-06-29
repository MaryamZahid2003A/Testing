#!/bin/bash

# Start Apache in background
service apache2 start

# Optional delay to wait for server to be up
sleep 5

# Run Selenium tests
python3 -m unittest -v tests/test_taskmanager.py

# Keep container running
tail -f /dev/null
