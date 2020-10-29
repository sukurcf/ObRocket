#!/usr/bin/env bash
cd /webapp
ng serve --host 0.0.0.0
python /app/process_basket.py 5000
