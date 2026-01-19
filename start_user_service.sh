#!/bin/bash
cd /home/ubuntu/fortis-api/api-agenda
source ../venv/bin/activate
export PYTHONPATH=/home/ubuntu/fortis-api/api-agenda
python3 user_service/start_user_service.py
