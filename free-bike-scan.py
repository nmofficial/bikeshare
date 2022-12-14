import urllib.request, json 
import time
from datetime import datetime

def get_bikes(data):
    new_free = {}
    bikes = data["data"]["bikes"]
    time = datetime.now()
    for elt in bikes:
        bike_id = elt.pop("bike_id")
        elt["time"] = time
        new_free[bike_id] = elt
        if elt["is_reserved"] == True:
            print(elt)
    return new_free

def check_free(old_free, new_free, busy):
    bike_ids = old_free.keys()
    for bid in bike_ids:
        if bid not in new_free:
            busy[bid] = old_free[bid]
    return busy

def check_busy(busy, free, trips):
    busy_bids = busy.keys()
    for bid in busy_bids:
        if bid in free:
            trips.append(busy[bid], free[bid])
            busy.pop(bid)
    return (trips, busy)
            
def main():
    with urllib.request.urlopen("https://gbfs.bird.co/dc") as url:
        data = json.load(url)
    
    free = get_bikes(data)
    busy = {}
    trips = []
    while True:
        with urllib.request.urlopen("https://gbfs.bird.co/dc") as url:
            new_data = json.load(url)
        new_free = get_bikes(new_data)
        busy = check_free(free, new_free, busy)
        trips, busy = check_busy(busy, new_free, trips)
        free = new_free
        print(datetime.now())
        print(trips)
        time.sleep(60)

if __name__ == "__main__":
    main()
