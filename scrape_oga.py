import urllib.request
import re

url = "https://opengameart.org/art-search-advanced?keys=isometric+farm"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    links = re.findall(r'href="(https://opengameart.org/sites/default/files/[^"]+\.(?:png|zip))"', html)
    for link in set(links):
        print(link)
except Exception as e:
    print("Error:", e)
