# worldevents

Scripts to scrap event data from rsoe-edis.org in json format and display them as plain text tables, per event category.

## Dependencies
- `bs4`
- `requests`
- `json`

Those are Python for the autogenerated `.py` scripts, they can installed with `pip3 install bs4 requests json`

## Usage
#### Installation

```bash
git clone https://git.teknik.io/matf/worldevents
cd worldevents
setup/./generate-code-scripts.sh
```
You may re-generate the `.py` scripts using `setup/./generate-code-scripts.sh` every time `setup/codes.txt` is manually updated.

#### Scrap data for one event category using the generated script (exemple for floods)

```bash
./FLD.py
```

#### Summarize scraped data in a simple plain text table
This will require additional dependencies: `pip3 install jello jtbl jq`

Then, paste this (replace `data/FLD.json` with the data file of your choice):

```bash
./show data/FLD.json
```

## To do
- Automate scrapping event codes into `setup/codes.txt`
- Add an option to scrap all categories at once instead of putting strain on the website with a request for every event category
- Fix show data as table
- Human readable categories, not only codes
- Better appending (avoid duplicates, add request date, merge into same json objects instead of creating new ones)

## Disclaimer
I was just reading about the `gemini` protocol and testing it with the cool `amfora` client, then stumbled upon `gemini://aetin.art/earth.gmi` and found the concept pretty cool, so I started playing with it. I am not a programmer, and I don't know how to write Python, so don't set your expectations too high.

These scripts are merely a way for me to play with web-scraping and Python for something I find useful, but I am not responsible for what you may use them for. Please just don't abuse using the scripts so that rsoe-edis.org doesn't start adding reCaptchas to their website.
