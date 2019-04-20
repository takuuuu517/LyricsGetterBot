import requests
import credentials
from bs4 import BeautifulSoup



def songInformation(search):
    # print("search")
    # print(search)
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + credentials.GeniusLyricsAccessToken}
    search_url = base_url + '/search'
    data = {'q': search}

    response = requests.get(search_url, data=data, headers=headers)
    return generateURL(response)

def generateURL(response):
    json = response.json()

    count = 0
    lists = []

    # print(len(json['response']['hits']))
    if len(json['response']['hits']) == 1:
        # print(json)
        lists.append("{}:{}".format(json['response']['hits'][0]['result']['title'],json['response']['hits'][0]['result']['primary_artist']['name']))
        return lists
    for hit in json['response']['hits']:
        s = "{}:{}".format(hit['result']['title'],hit['result']['primary_artist']['name'])

        # print(songinfohelper(s))
        if len(songinfohelper(s)) <= 20:
            lists.append(songinfohelper(s))
            count += 1;
        if count == 5:
            break
    if not lists:
        lists.append("ごめんなかった")
    return lists

def songinfohelper(song):
    parenthesis = False
    start = 0
    end = 0
    b = True
    count = 0
    for c in song:
        if c == ':':
            b = False
        elif c == ' ' and b == False:
            break;
        elif c == '(':
            parenthesis = True
            start = count
        elif c == ')':
            end = count
        count += 1

    if parenthesis:
        return song[0:start-1] + song[end+1: count]
    return song[0:count]

def getUrl(realsearch):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + credentials.GeniusLyricsAccessToken}
    search_url = base_url + '/search'
    data = {'q': realsearch}

    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()

    # print(json['response']['hits'][0]['result']['url'])
    return json['response']['hits'][0]['result']['url']



def getLyricstext(url):
    lyricspage = requests.get(url)
    html = BeautifulSoup(lyricspage.text, 'html.parser')
    lyricstext = html.find('div', class_='lyrics').get_text()
    # print(lyricstext)
    return lyricstext


def test():
    list = getUrl("yonedu:lemon")
    # print(getLyricstext(list))
    # generateURL(res)
    return None
    # return //getLyricstext("https://genius.com/Kenshi-yonezu-lemon-lyrics")
