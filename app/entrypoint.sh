#!/bin/bash
gunicorn -b 0.0.0.0:10500 --reload --access-logfile gunicorn_access.log --error-logfile gunicorn_error.log --log-level debug --timeout 120 pitemp_api &
python3 pitemp.py &
