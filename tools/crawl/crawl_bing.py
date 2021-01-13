from bs4 import BeautifulSoup
import os
import json
import urllib.request, urllib.error, urllib.parse
from requests.utils import requote_uri


"""Bing 전용 다운로더"""


def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url, headers=header)),
        'html.parser')


def url_encode(str):
  return urllib.parse.quote(str)


def url_decode(str):
  return urllib.parse.unquote(str)


max_cnt = 100
query = ""
query= query.split()
query='+'.join(query)

encode_query = url_encode(query)

DIR="images"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

search_index = 1
cnt = 1
ActualImages = []
checked_same_images = []
for _ in range(max_cnt):
    url = "http://www.bing.com/images/search?q=" + encode_query + "&FORM=HDRSC2" + "&first=" + str(search_index)
    soup = get_soup(url,header)

    size = 0
    for a in soup.find_all("a",{"class":"iusc"}):
        try:
            mad = json.loads(a["mad"])
            turl = mad["turl"]
        except:
            turl = ""

        try:
            m = json.loads(a["m"])
            murl = m["murl"]
        except:
            murl = ""

        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]

        if image_name in checked_same_images:
            continue

        checked_same_images.append(image_name)
        print(image_name)

        img_name = query+"_"+str(cnt)+".jpg"
        ActualImages.append((img_name, turl, murl))
        cnt += 1
        size += 1

    if size == 0:
        break

    search_index += len(ActualImages)

print("there are total" , len(ActualImages), "images")

if not os.path.exists(DIR):
    os.mkdir(DIR)

DIR = os.path.join(DIR, query.split()[0])
if not os.path.exists(DIR):
    os.mkdir(DIR)

for i, (image_name, turl, murl) in enumerate(ActualImages):
    try:
        if turl == "":
            murl = requote_uri(murl)
            raw_img = urllib.request.urlopen(murl).read()
        else:
            turl = requote_uri(turl)
            raw_img = urllib.request.urlopen(turl).read()

        cntr = len([i for i in os.listdir(DIR) if image_name in i]) + 1

        f = open(os.path.join(DIR, image_name), 'wb')
        f.write(raw_img)
        f.close()
    except Exception as e:
        print("could not load : " + image_name)
        print(e)
