#!/bin/bash

# Start the PHP server to host your web app
php -S 0.0.0.0:80 -t /var/www/html &

# Wait for the server to come up
sleep 5

# Run Selenium tests
python3 -m unittest -v tests/test_taskmanager.py
