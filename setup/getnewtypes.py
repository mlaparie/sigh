#!/usr/bin/env python3
# Update event types from rsoe.edis.org
# and merge with local list used to scrape
# matf & cassandra-as-a-service
# Dependencies: bs4, requests

import os
import requests
from bs4 import BeautifulSoup


wedir = os.environ["WE_DIR"]


def scrape_html(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, "lxml")
    return soup


def get_event_types(soup):
    listOfEventTypes = []
    for subsection in soup.findAll(class_="sub-section"):
        listOfEventTypes.append(subsection.get("id")[-3:])
        listOfEventTypes.sort()
    return listOfEventTypes


html = scrape_html("https://rsoe-edis.org/eventList")
eventsList = get_event_types(html)


with open(wedir+'/setup/types.txt', 'r+') as f:
    typesList = f.readlines()
    typesList = [line.strip() for line in typesList]
    eventsList.sort()
    unique = list(set(typesList + eventsList))
    unique.sort()
    f.seek(0)
    f.write("\n".join(i for i in unique))
    f.truncate()
    f.close()

print(f'\033[32;1m✔\033[0m Found {len(eventsList)} active event',
      'types, local list updated',
      f'(+{len(unique)-len(typesList)},',
      f'{len(unique)} total).')
