#!/bin/bash
# Start Apache in the background
apachectl -D FOREGROUND &
# Wait a bit to ensure Apache starts
sleep 5
# Now run the test suite
python3 -m unittest -v tests/test_taskmanager.py
