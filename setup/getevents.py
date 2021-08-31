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
sublistToSearch = None


def scrape_html(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, "lxml")
    return soup


def get_event_cards(soup, eventsList):
    global sublistToSearch
    sublistToSearch = get_sublist_from_args(eventsList)
    eventCards = soup.find(id="sub-{threeLetterCode}".format(threeLetterCode=sublistToSearch))
    eventCards = eventCards.find_all("div", {"class": "event-card"})
    return eventCards


def get_fields_from_event_card(card):
    fieldsToFind = ["title", "time", "location", "details"]
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
    fieldsToFind = ["latitude", "longitude", "source", "category"]
    fieldData = {}
    for f in fieldsToFind:
        if f == "source":
            fieldData[f] = soup.find(class_="part-bigger").find("a", href=True)["href"]
        elif f == "category":
            fieldData[f] = soup.find(class_="category-text").text.strip()
        else:
            fieldData[f] = soup.find(id=f).text.strip()
    return fieldData


def get_sublist_from_args(eventsList):
    parser = argparse.ArgumentParser(description='Scrape events data from rsoe-edis.org')
    parser.add_argument("-s", required=True, dest="sublist", choices=eventsList, help="get events for queried subcategory")
    return parser.parse_args().sublist


with open(wedir+'/setup/subcategories.txt', 'r') as f:
    eventsList = f.readlines()
    eventsList = [line.strip() for line in eventsList]


try:
    html = scrape_html("https://rsoe-edis.org/eventList")
    eventCards = get_event_cards(html, eventsList)

    for card in eventCards:
        print(json.dumps(get_fields_from_event_card(card)), file=open(wedir+'/data/'+sublistToSearch+'.json', 'a'))

    print(f'{len(eventCards)} ' f'{sublistToSearch} event(s)… ', end='')
    print(f'\033[32;1m✔\033[0m Appended {len(eventCards)} event(s) to {wedir}/data/{sublistToSearch}.json.')

except Exception as e:
    print(f'\033[31;1m⨉\033[0m No {sublistToSearch} events to scrap at the moment.', e)
