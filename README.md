# simple-flask-api

## API Specifications:

- Endpoint #1 - /getall - send all data as json
  
- Endpoint #2 - /search?station=xyz - send data of station names that match "xyz"
  
- Endpoint #3 - /distance?from=id1&to=id2 - send distance between two given station codes on the same line

## Assumptions:

- API is read-only. We are only performing requests to retrieve data.

## Edge Case:

- CSV file is updated externally. (could be solved using file system monitoring)

## Libraries used:

- Flask: Python library to develop lightweight APIs. As this was a tiny API, using Django and other heavy alternatives didn't seem viable.
  
- Pandas: I'm aware of the fact that this a heavy library and can increase the server boot up time by a considerable amount, but it's much more relaible than the standard built in python library for dealing with csvs. 
  
## Setup:

- Please make sure python 3.7x is installed in your system.
  
- Initialise and activate a new virtual environment
  
- Change current directory to the project 
  
- Install dependencies using the command: pip install -r requirements.txt
  
- Update .env file with variable values corrsponding to your system and local dev setup
  
- Start flask server using command: python app.py

## Testing:

- Get All Endpoint:  http://localhost:5000/getAll
  
- Search Endpoint:   http://localhost:5000/search?station=xyz
  
- Distance Endpoint: http://localhost:5000/distance?startStation=MTCN&endStation=MCPT
