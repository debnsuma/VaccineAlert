from datetime import date
import time
from pprint import pprint as pp

import yaml
import pathlib
import requests
import json

cwd = str(pathlib.Path().absolute())
config_path = pathlib.os.path.join(cwd, 'config.yml')

with open(config_path) as f:
    config_data = yaml.load(f, Loader=yaml.FullLoader)
    
current_data = date.today().strftime("%d-%m-%y")

BASE_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}"
URL = BASE_URL.format(config_data['pincode'], current_data)

# Faking the browser header (http://www.useragentstring.com/pages/useragentstring.php?name=Chrome) 
browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

response = requests.get(URL, headers=browser_header)
data = json.loads(response.text)

center = {}
centers = [] 
if data["sessions"]:
    for slots in data["sessions"]:
        center["Center Name"] = slots["center_id"]
        center["Address"] = slots["address"]
        center["Pin"] = slots["pincode"]
        center["Date"] = slots["date"]
        center["Vaccine Name"] = slots["vaccine"]
        center["Available Capacity"] = slots["available_capacity"]
        center["Available Slot"] = slots["slots"]   
        
        # for streamlite
        center["lat"] = slots["lat"] 
        center["long"] = slots["long"] 
        
        centers.append(center)
else:
    centers = {"Status " : "Noting Available"}
        
        
pp(centers)

