#!/usr/bin/env bash
ng serve /webapp --host 0.0.0.0
python /app/process_basket.py 5000
