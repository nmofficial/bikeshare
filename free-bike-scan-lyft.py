import urllib.request, json 
import time
from datetime import datetime

#lyft: "https://s3.amazonaws.com/lyft-lastmile-production-iad/lbs/dca/free_bike_status.json"
#bird: https://gbfs.bird.co/dc

def get_bikes(data):
    new_free = {}
    bikes = data["data"]["bikes"]
    time = datetime.now()
    for elt in bikes:
        bike_id = elt.pop("name")
        elt["time"] = time
        new_free[bike_id] = elt
        if elt["is_reserved"] != 0:
            print(elt)
    return new_free

def check_change(old_free, new_free):
    change = {}
    bike_ids = old_free.keys()
    for bid in bike_ids:
        if bid not in new_free:
            change[bid] = old_free[bid]
    return change

def main():
    with urllib.request.urlopen("https://gbfs.bird.co/dc") as url:
        data = json.load(url)
    
    free = get_bikes(data)
    disappear_file = open("disappear.txt", 'a')
    reappear_file = open("reappear.txt", 'a')
    while True:
        with urllib.request.urlopen("https://gbfs.bird.co/d") as url:
            new_data = json.load(url)
        new_free = get_bikes(new_data)
        disappear = check_change(free, new_free)
        reappear = check_change(new_free, free)
        print(disappear, file=disappear_file)
        print(reappear, file=reappear_file)
        print(datetime.now())
        print(disappear.keys())
        print(reappear.keys())
        time.sleep(60)

if __name__ == "__main__":
    main()
