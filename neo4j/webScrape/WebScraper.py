import requests
import json
import urllib
import numpy
global var1
global titlelist 
titlelist = []
global desclist
desclist = []
global linklist 
linklist = []
global contentlist
contentlist = []

# def uptoserver(title_, desc_, link_):
#     # url = 'http://httpbin.org/post'
    # files = {'file': open('final.txt', 'r+')}

    # r = requests.post(url, files=files)
    # print(r.text)
    # print(response.status_code)
    # print(response.text)

def parser(list_):
    for i in range(len(list_)):
        split_ = list_[i].split('\n')
        title = split_[0]
        desc = split_[1]
        link = split_[2]
        titlelist.append(title)
        desclist.append(desc)
        linklist.append(link)
        with open('final.txt', 'w') as file_:
            file_.writelines([title, desc, link])
        # uptoserver(title, desc, link)
        print(title)
        print(desc)
        print(link)
        print('\n')        
    

def scrape(pname):
    tag = pname + " 2020 news"
    tag = tag.replace(' ', '+')
    query = {
        "q": tag,
        "num": 7,
        "lr": "lang_en"
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
    # for i in len(filtered)
    filtered = numpy.array(filtered)
    for x in filtered:
        # splitEntry = var1[1].split(':')
        if 'News' in x['title'] or 'news' in x['title'] or 'latest' in x['title'] or 'The Guardian' in x['title']:
            continue
        with open('clean.txt', 'w') as file:
                file.write(json.dumps(x['title']))
                file.write('\n')
                file.write(json.dumps(x['description']))
                file.write('\n')
                file.write(json.dumps(x['link']))
                file.write('\n')
                file.write('\n')
    
        f = open('clean.txt', 'r')
        contents = f.read()
        contentlist.append(contents)
        print('\n')

    parser(contentlist)
    # print(contentlist)
    return contentlist
    # print('Recent player news:', *filtered, sep='\n- ')

# username = "Bruno Fernandes"
# scrape(username)
# # print(titlelist, desclist, linklist)
