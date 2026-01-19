#!/bin/bash
cd /home/ubuntu/fortis-api/api-agenda
source ../venv/bin/activate
export PYTHONPATH=/home/ubuntu/fortis-api/api-agenda
python3 location_service/start_location_service.py
