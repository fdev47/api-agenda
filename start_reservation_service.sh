#!/bin/bash
cd /home/ubuntu/fortis-api/api-agenda
source ../venv/bin/activate
export PYTHONPATH=/home/ubuntu/fortis-api/api-agenda
python3 reservation_service/start_reservation_service.py
