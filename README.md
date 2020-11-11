# ObjectRocket task - Sukumar P.
https://gist.github.com/jbartels/d75a9f5282abebe071694723a5f25f0e

## Overview:
This app depends on both Flask app and Angular app.

Used **rackspacedot/python38** as base image.

This repo contains Flask app and test cases. 

Angular app is hosted on separate repo - https://github.com/sukurcf/ObRocket-UI.git to keep it modular.

Users can add items from list available. 

Total and price of each item, coupons applied will be updated automatically once the user hits enter or click the **ADD ITEM** button in UI.

Implemented 3 out of 4 coupons - **BOGO**, **APPL**, **CHMK**. 
Couldn't implement 4th coupon **APOM** as I couldn't understand the requirement clearly as there were no example cases in test cases.

I thought of using database for storing items. But realised that it becomes much complex for this simple use case.

## Pre-requisites:
1. Docker

## Steps to run.
Run the commands in **powershell**. 

1. Build the docker image using the Dockerfile provided and following command:
   
   `docker build -t objectrocket:sukurcf .`
2. Run the docker container using following command.
   
   `docker run -p 5000:5000 -p 4200:4200 objectrocket:sukurcf`
3. API server and Angular app will be up and running. Open the browser and hit http://localhost:4200/ to see Angular app. 
   You can add new items from UI and the list will be automatically updated and coupons will be automatically applied.
4. After cloning the repo locally, run test cases locally using below command:
   
   `python test_process_basket.py`
   
![Farmer's Market](https://github.com/sukurcf/ObRocket/blob/main/farmers_market.JPG)

## Note: 
Please let me know if 4th coupon **APOM** also need to be implemented. Also please provide few example scenarios for the same to understand it better. 
