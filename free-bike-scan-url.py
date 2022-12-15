import urllib.request, json 
import time
from datetime import datetime
import copy
import sys

#lyft: "https://s3.amazonaws.com/lyft-lastmile-production-iad/lbs/dca/free_bike_status.json"
#bird: https://gbfs.bird.co/dc
#lyft bay wheels SF: https://gbfs.baywheels.com/gbfs/fr/free_bike_status.json 

def get_bikes_bid(data):
    new_free = {}
    bikes = data["data"]["bikes"]
    time = datetime.now()
    for elt in bikes:
        bike_id = elt.pop("bike_id")
        elt["time"] = time
        new_free[bike_id] = elt
        if elt["is_reserved"] != 0:
            print(elt)
    return new_free

def get_bikes_coord(data):
    new_free = {}
    bikes = data["data"]["bikes"]
    time = datetime.now()
    for elt in bikes:
        lat = elt.pop("lat")
        lon = elt.pop("lon")
        elt["time"] = time
        new_free[(lat, lon)] = elt
        if elt["is_reserved"] != 0:
            print(elt)
    return new_free

def check_change(old_bid, old_coord, new_bid, new_coord):
    change = {}
    coords = old_coord.keys()
    for coord in coords:
        if coord not in new_coord:
            bid = old_coord[coord]["bike_id"]
            if bid not in new_bid:
                change[coord] = old_coord[coord]
    return change

def main():
    url_data = sys.argv[1]
    file_name = sys.argv[2]
    with urllib.request.urlopen(url_data) as url:
        data = json.load(url)
    data2 = copy.deepcopy(data)
    
    old_bid = get_bikes_bid(data)
    old_coord = get_bikes_coord(data2)
    print(old_coord)
    disappear_file = open(file_name + "disappear.txt", 'a')
    reappear_file = open(file_name + "reappear.txt", 'a')
    while True:
        with urllib.request.urlopen(url_data) as url:
            new_data = json.load(url)
        new_data2 = copy.deepcopy(new_data)
        new_bid = get_bikes_bid(new_data)
        new_coord = get_bikes_coord(new_data2)
        disappear = check_change(old_bid, old_coord, new_bid, new_coord)
        reappear = check_change(new_bid, new_coord, old_bid, old_coord)
        print(disappear, file=disappear_file)
        print(reappear, file=reappear_file)
        print(datetime.now())
        print(disappear.keys())
        print(reappear.keys())
        time.sleep(60)
        old_bid = new_bid
        old_coord = new_coord

if __name__ == "__main__":
    main()
