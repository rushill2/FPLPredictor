import requests
import json
import urllib

username_ = "Harry Kane"
tag = username_ + " 2020 news"
tag = tag.replace(' ', '+')
query = {
    "q": tag,
    "num": 5
}
url = "https://google-search3.p.rapidapi.com/api/v1/search/" + urllib.parse.urlencode(query)
# print(url)

headers = {
    'x-rapidapi-key': "826a1cda37msh041d96ed8e5edb9p18ef04jsn660d43e6890d",
    'x-rapidapi-host': "google-search3.p.rapidapi.com"
    }    
copy_data = {}
response = requests.request("GET", url, headers=headers)
# print(response.json())
output = response.json()
json_object = json.dumps(output, indent = 4) 
with open("data.json", "w") as outfile: 
    outfile.write(json_object) 
dict_ = eval(json_object)


filtered = dict_['results']
print(filtered)
print('\n')
# for i in len(filtered)
    
print('Recent player news:', *filtered, sep='\n- ')

