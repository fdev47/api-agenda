#!/bin/bash
cd /home/ubuntu/fortis-api/api-agenda
source ../venv/bin/activate
export PYTHONPATH=/home/ubuntu/fortis-api/api-agenda
python3 auth/start_auth_service.py
