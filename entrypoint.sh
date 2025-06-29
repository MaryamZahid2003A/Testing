#!/bin/bash

# Wait for MySQL or other services (optional but good)
sleep 5

# Run tests
python3 -m unittest -v tests/test_taskmanager.py

# Start Apache in the foreground (this keeps container alive)
exec apachectl -D FOREGROUND
