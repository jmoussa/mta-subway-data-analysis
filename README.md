# MTA Subway Tracker

## Setup
This project is setup using Anaconda to setup simply run:
```
conda env create -f environment.yml
```

Before running the `get_mta_data.py` script copy `base.template.json` into a `base.json` and supply the necessary fields.
- mta_api_key: API key for the MTA found here https://datamine.mta.info/user (you need to register)

## Run the main script
```
python get_mta_data.py
```
- Takes no inputs.
- Outputs 
    * `train_real_time_data.csv`: dataframe of the realtime location of subway cars with extra info
    * `mta.html`: html file that plots the real time location of the subway cars


## Project Description
This project is run through a single script `get_mta_data.py` which requires a `base.json` file to be available (use `base.template.json` as a temaplate).

The script returns a csv of real time data of where each trainline stops and then spits out an html page that you can then open and view them plotted on a Google Maps (dev version) map.

Currently the subway lines supported are the 1-6 and N, R, Q, and W lines but the rest can be added easily from https://datamine.mta.info/list-of-feeds
