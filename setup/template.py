#!/usr/bin/env python3
# Scrape event information from rsoe.edis.org
# Copyright aetin, see gemini://aetin.art/earth.gmi
# Modified by matf
# Dependencies: bs4, requests, json

import os
import requests
import json
from bs4 import BeautifulSoup

wedir = os.environ["WE_DIR"]
if __name__ == "__main__":
    res = requests.get("https://rsoe-edis.org/eventList")
    content = res.text
    soup = BeautifulSoup(content, "lxml")
    sreplacemes = soup.find(id="subList-replaceme")

    try:
        replaceme = [x.text.replace('\n', '').strip(' ') for x in sreplacemes.findAll("td", {"class": "eventDate"})]
        locs = [x.text.replace('\n', '').strip(' ') for x in sreplacemes.findAll("td", {"class": "location"})]
        titles = [x.text.replace('\n', '').strip(' ') for x in sreplacemes.findAll("h5", {"class": "title"})]
        details = [x.find("a", href=True)["href"] for x in sreplacemes.findAll("td", {"class": "details"})]

        result = []

        for url in details:
            sourceurls = requests.get(url)
            sourcecontent = sourceurls.text
            soupsource = BeautifulSoup(sourcecontent, "lxml")
            source = [x.find("a", href=True)["href"] for x in soupsource.findAll("div", {"class": "part-bigger"})]
            lat = [x.text.replace('\n', '').strip(' ') for x in soupsource.findAll("p", {"id": "latitude"})]
            lon = [x.text.replace('\n', '').strip(' ') for x in soupsource.findAll("p", {"id": "longitude"})]

            json_data = {"Time": replaceme, "Location": locs, "Title": titles, "Details": details, "Source": source, "Lat": lat, "Lon": lon}

            for t, l, m, d, s, y, x in zip(json_data["Time"], json_data["Location"], json_data["Title"], json_data["Details"], json_data["Source"], json_data["Lat"], json_data["Lon"]):
                result.append({"Time": t, "Location": l, "Title": m, "Details": d, "Source": s, "Lat": y, "Lon": x})

        result = json.dumps(result)
        print(result, file=open(wedir+'/data/replaceme.json', 'a'))
        print(f' \033[32;1m✔\033[0m Appended {len(replaceme)} event(s) to {wedir}/data/replaceme.json.')

    except Exception as e:
        print(' \033[31;1m⨉\033[0m No replaceme events to scrap at the moment.', e)
