# ObjectRocket task - Sukumar P.

## Pre-requisites:
1. Docker

## Steps to run.
1. Build the docker image using the Dockerfile provided and following command:
   
   `docker build -t objectrocket:sukurcf .`
2. Run the docker container using following command and also provide the products in basket as input to the container's entry point as below.
    
    `docker run objectrocket:sukurcf process_basket.py CH1,AP1,AP1,AP1,MK1`
3. You will see output in the below format:
    
    `Product prices:  [3.11, 4.5, 4.5, 4.5, 0]` 
    `Total price expected: $ 16.61`
    `Coupons applied:  ['APPL', 'APPL', 'APPL', 'CHMK']`
4. Run tests.py using below command:
    
    `docker run objectrocket:sukurcf tests.py`