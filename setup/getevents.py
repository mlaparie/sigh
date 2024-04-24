#!/usr/bin/env python3
# Scrape event information from rsoe.edis.org
# matf & cassandra-as-a-service
# Dependencies: bs4, requests, json, argparse

import os
import requests
import json
from bs4 import BeautifulSoup
import argparse


wedir = os.environ["WE_DIR"]
typeToSearch = None


def scrape_html(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, "lxml")
    return soup


def get_event_cards(soup, eventsList):
    global typeToSearch
    typeToSearch = get_type_from_args(eventsList)
    eventCards = soup.find(id="sub-{threeLetterCode}".format(threeLetterCode=typeToSearch))
    eventCards = eventCards.find_all("div", {"class": "event-card"})
    #print(f'{len(eventCards)} ' f'{typeToSearch} event(s)… ', end='')
    return eventCards


def get_fields_from_event_card(card):
    fieldsToFind = ["time", "title", "location", "details"]
    fieldData = {}
    for f in fieldsToFind:
        if f == "details":
            fieldData[f] = card.find("a", href=True)["href"]
        elif f == "time":
            fieldData[f] = card.find(class_="eventDate").text.strip()
        else:
            fieldData[f] = card.find(class_=f).text.strip()
    fieldData.update(get_additional_detail(fieldData["details"]))
    return fieldData


def get_additional_detail(detailUrl):
    soup = scrape_html(detailUrl)
    fieldsToFind = ["source", "category", "latitude", "longitude", "description"]
    fieldData = {}
    for f in fieldsToFind:
        if f == "source":
            fieldData[f] = soup.find(class_="part-bigger").find("a", href=True)["href"]
        elif f == "category":
            fieldData[f] = soup.find(class_="category-text").text.strip()
        elif f == "description":
            fieldData[f] = soup.find(class_="event-description").text.strip()
        else:
            fieldData[f] = soup.find(id=f).text.strip()
    return fieldData


def get_type_from_args(eventsList):
    parser = argparse.ArgumentParser(description='Scrape events data from rsoe-edis.org')
    parser.add_argument("-t,", "--type", required=False, dest="type", help="get events for queried type (three-letter code)")
    return parser.parse_args().type


with open(wedir+'/setup/types.txt', 'r') as f:
    eventsList = f.readlines()
    eventsList = [line.strip() for line in eventsList]


try:
    html = scrape_html("https://rsoe-edis.org/eventList")
    eventCards = get_event_cards(html, eventsList)

    for card in eventCards:
        print(json.dumps(get_fields_from_event_card(card)), file=open(wedir+'/data/'+typeToSearch+'.json', 'a'))

    print(f'\033[32;1m✔\033[0m {len(eventCards)} added to {wedir}/data/{typeToSearch}.json.')

except Exception as e:
    print(f'\033[31;1m𐄂\033[0m 0 active at the moment.')
