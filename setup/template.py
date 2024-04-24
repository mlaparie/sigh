#!/usr/bin/env python3
# Scrap event information from rsoe.edis.org
# Copyright aetin, see gemini://aetin.art/earth.gmi
# Modified by matf
# Dependencies: bs4, requests, json

import os
import requests
import json
from bs4 import BeautifulSoup

wedir=os.environ["WE_DIR"]
if __name__ == "__main__":
    res = requests.get("https://rsoe-edis.org/eventList")
    content = res.text
    soup = BeautifulSoup(content, "lxml")
    sreplacemes = soup.find(id="subList-replaceme")
    replaceme = [ x.text.replace('\n', '').strip(' ')  for x in  sreplacemes.findAll("td", {"class": "eventDate"}) ]
    locs = [ x.text.replace('\n', '').strip(' ')  for x in  sreplacemes.findAll("td", {"class": "location"}) ]
    titles = [ x.text.replace('\n', '').strip(' ')  for x in  sreplacemes.findAll("h5", {"class": "title"}) ]
    details = [ x.find("a", href=True)["href"]  for x in  sreplacemes.findAll("td", {"class": "details"}) ]
    json_data = json.dumps({"Date": replaceme, "Location": locs, "Title": titles, "Details": details})
    print(json_data, file=open(wedir+'/data/replaceme.json', 'a'))
    print('Appended data to '+wedir+'/data/replaceme.json. \033[32;1m✔\033[0m')
    print(len(json_data[0]['Date'])+' events.')
