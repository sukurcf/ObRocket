#!/usr/bin/env bash
python /app/process_basket.py 5000 &
cd /webapp
ng serve --host 0.0.0.0

