#!/bin/bash
cd /home/ubuntu/fortis-api/api-agenda
source ../venv/bin/activate
export PYTHONPATH=/home/ubuntu/fortis-api/api-agenda
python3 api_gateway/start_api_gateway.py
