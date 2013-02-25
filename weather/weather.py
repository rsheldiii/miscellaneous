import requests
import sys

def forecast(state, city):
    base_url = "http://weather.noaa.gov/pub/data/forecasts/city/%s/%s.txt"
    city = city.lower().replace(" ", "_")
    result = requests.get(base_url % (state, city))
    if result.ok:
        return result.content
    else:
        #result.raise_for_status()
        print("could not find %s, check formatting:\n %s" % (city,base_url % (state,city)))

if(len(sys.argv)>2):
    print(forecast(sys.argv[1],sys.argv[2]))
else:
    print("usage: weather state city. State is 2 letter postal code")
