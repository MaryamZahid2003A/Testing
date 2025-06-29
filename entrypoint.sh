#!/bin/bash

# Start Apache in the background
apache2ctl start

# Wait a few seconds to ensure Apache is ready
sleep 5

# Run tests (optional: adjust path if tests are elsewhere)
python3 -m unittest -v tests/test_taskmanager.py

# Keep the container alive so logs can be checked
tail -f /dev/null
