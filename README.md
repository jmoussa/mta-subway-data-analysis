# MTA Subway Tracker

This project is run through a single script `get_mta_data.py` which requires a `base.json` file to be available (use base.template.json as a temaplate).

The script returns a csv of real time data of where each trainline stops and then spits out an html page that you can then open and view them plotted on a Google Maps (dev version) map.

Currently the subway lines supported are the 1-6 and N, R, Q, and W lines but the rest can be added easily from https://datamine.mta.info/list-of-feeds
