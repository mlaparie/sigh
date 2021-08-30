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
    try:
        replaceme = [ x.text.replace('\n', '').strip(' ')  for x in  sreplacemes.findAll("td", {"class": "eventDate"}) ]
        locs = [ x.text.replace('\n', '').strip(' ')  for x in  sreplacemes.findAll("td", {"class": "location"}) ]
        titles = [ x.text.replace('\n', '').strip(' ')  for x in  sreplacemes.findAll("h5", {"class": "title"}) ]
        details = [ x.find("a", href=True)["href"]  for x in  sreplacemes.findAll("td", {"class": "details"}) ]
        json_data = {"Date": replaceme, "Location": locs, "Title": titles, "Details": details}

        result = []
        for d, l, t, x in zip(json_data["Date"], json_data["Location"], json_data["Title"], json_data["Details"]):
            result.append({"Date": d, "Location": l, "Title": t, "Details": x})

        result = json.dumps(result)
        print(result, file=open(wedir+'/data/replaceme.json', 'a'))
        print(f' \033[32;1m✔\033[0m Appended {len(replaceme)} event(s) to {wedir}/data/replaceme.json.')
    except Exception as e:
      print(' \033[31;1m⨉\033[0m No replaceme events to scrap at the moment.')
