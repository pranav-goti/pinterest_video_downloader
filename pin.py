import requests as re
from bs4 import BeautifulSoup
import json
import urllib
import sys
import random
import string
import os

def getVideo(JO):
    if 'resourceResponses' in JO.keys():
        if type(JO['resourceResponses']) == type(list()):
            ans = JO['resourceResponses'][0]['response']['data']['story_pin_data']['pages'][0]['blocks'][0]['video']['video_list']
            k = list(ans.keys())
            url = ans[k[0]]['url']
            if url.endswith('.mp4'):
                return (True,url)
            else:
                return (False,None)

def getVideo2(JO):
    if 'resourceResponses' in JO.keys():
        if type(JO['resourceResponses']) == type(list()):
            ans = JO['resourceResponses'][0]['response']['data']['videos']['video_list']
            k = list(ans.keys())
            url = ans[k[0]]['url']
            if url.endswith('.mp4'):
                return (True,url)
            else:
                return (False,None)

def downloadVideo(url):
    sulon = random.randint(0,5)
    vidName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=sulon))
    vidName = 'C:\\downloads\\' +vidName + '.mp4'
    newpath = r'C:\downloads' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    urllib.request.urlretrieve(url, vidName)
    return vidName

def getEndpointURL(endpoint):
    res = re.get(endpoint)
    soup = BeautifulSoup(res.text,"html.parser")
    li = soup.find('body')
    scr = li.find_all('script')
    txt = str(scr[-1])
    ind = txt.index('>')
    txt = txt[ind+1:]
    txt = txt[:-9]
    JO = json.loads(txt)
    ans = JO['context']['current_url'].split('/')
    ans = ans[0]+ '/' + ans[1] + '/' + ans[2] + '/' + ans[3] + '/' + ans[4]
    return ans

if len(sys.argv) == 2:
    endpoint = sys.argv[1]
    try:
        index = endpoint.index('pin.it')
    except Exception as e:
        index = 0
    if index > 0:
        endpoint = getEndpointURL(endpoint)
    print('++++++++++++++++++++++++++++++')
    print(endpoint)
    res = re.get(endpoint)
    soup = BeautifulSoup(res.text,"html.parser")
    li = soup.find('body')
    scr = li.find_all('script')
    txt = str(scr[1])
    ind = txt.index('>')
    txt = txt[ind+1:]
    txt = txt[:-9]
    JO = json.loads(txt)

    try:
        res, url = getVideo(JO)
        if res:
            pth = downloadVideo(url)
            print(f'video has been downloaded at {pth} location.')
            exit()
    except Exception as e:
        print('Launching Another Function...')

    try:
        res, url = getVideo2(JO)
        if res:
            pth = downloadVideo(url)
            print(f'video has been downloaded at {pth} location.')
            exit()
    except Exception as e:
        print('Sorry !! Not able to download , Please Post Comment on Github')
        print('We\'ll Definetly try to Resolve your issue.')
    