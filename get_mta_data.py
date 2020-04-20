from google.transit import gtfs_realtime_pb2
from datetime import datetime
import pandas as pd
import requests
import coloredlogs
import logging
import gmplot
import json

coloredlogs.install(level="DEBUG", fmt="%(asctime)s %(hostname)s %(name)s %(message)s")

FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def main():
    stops_df = pd.read_csv("./stops.csv")
    routes_df = pd.read_csv("./routes.csv")

    config = parse_json("./base.json")
    mta_api_key = config["mta_api_key"]

    # 1-6 lines
    feed = get_feed(feed_id="1", api_key=mta_api_key)
    # N R Q W lines
    feed2 = get_feed(feed_id="16", api_key=mta_api_key)

    feeds_array = [feed, feed2]
    last_stops_df = get_last_stops_df(feeds_array, stops=stops_df, routes=routes_df)

    latitude_list = last_stops_df["lattitude"].to_list()
    longitude_list = last_stops_df["longitude"].to_list()
    plot_lat_long(latitude_list, longitude_list)


def get_feed(feed_id="1", api_key=None):
    if api_key is not None:
        feed = gtfs_realtime_pb2.FeedMessage()
        url1 = f"http://datamine.mta.info/mta_esi.php?key={api_key}&feed_id={feed_id}"
        response1 = requests.get(url1, allow_redirects=True)
        feed.ParseFromString(response1.content)
        return feed
    else:
        raise Exception("No API Key Found, check base.json for `mta_api_key` field")


def parse_json(file_name):
    json_file = open(file_name)
    data = json.load(json_file)
    return data


def get_last_stops_df(feeds_array, stops=None, routes=None):
    if stops is not None and routes is not None:
        master_df = {}
        master_df["route_id"] = []
        master_df["route_name"] = []
        master_df["time"] = []
        master_df["stop_name"] = []
        master_df["lattitude"] = []
        master_df["longitude"] = []

        for feed in feeds_array:
            for entity in feed.entity:
                if entity.HasField("trip_update") and len(entity.trip_update.stop_time_update) > 0:
                    route_id = entity.trip_update.trip.route_id
                    route_name = " ".join(
                        routes[routes["route_id"] == route_id].route_long_name.to_string().split(" ")[4:]
                    )
                    logger.info(f"LINE: {route_id} {route_name}")

                    last_idx = len(entity.trip_update.stop_time_update) - 1
                    last_elem = entity.trip_update.stop_time_update[last_idx]
                    time = datetime.fromtimestamp(last_elem.arrival.time)
                    str_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"TIME: {str_time}")

                    stop_name = " ".join(
                        stops[stops["stop_id"] == last_elem.stop_id].stop_name.to_string().split(" ")[4:]
                    )
                    logger.info(f"STOP: {stop_name}\n")

                    lat = stops[stops["stop_id"] == last_elem.stop_id].stop_lat.values[0]
                    long = stops[stops["stop_id"] == last_elem.stop_id].stop_lon.values[0]

                    master_df["route_id"].append(route_id)
                    master_df["route_name"].append(route_name)
                    master_df["time"].append(str_time)
                    master_df["stop_name"].append(stop_name)
                    master_df["lattitude"].append(lat)
                    master_df["longitude"].append(long)

        df = pd.DataFrame(master_df)
        df.to_csv("./train_real_time_data.csv")
        logger.info(df)
        return df
    else:
        raise Exception("Missing routes and stops dataframes")


def plot_lat_long(latitude_list, longitude_list):
    # init google maps
    gmap = gmplot.GoogleMapPlotter(40.7128, -74.0060, 12)
    gmap.scatter(latitude_list, longitude_list, "#FF0000", size=100, marker=False)
    # pass absolute path
    gmap.draw("./mta.html")


if __name__ == "__main__":
    main()
