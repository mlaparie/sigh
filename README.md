# worldevents (`we`)

Script to scrap, save and print event data from rsoe-edis.org, per event category.

## Installation
#### Dependencies
- `bs4`
- `requests`
- `json`
- `jello`
- `jtbl`

Those are Python dependencies for the autogenerated `.py` scripts, they can be installed with `pip3 install bs4 requests json jello jtbl`

#### Generate scripts

```bash
git clone https://git.teknik.io/matf/worldevents
cd worldevents
./we --setup
ln -s we $HOME/.local/bin/we # Optional, to make `we` accessible from anywhere
```

You may re-generate the `.py` scripts using `we --setup` every time `setup/codes.txt` is manually updated.
Automatically updating codes is not supported yet.

## Usage

```plain
$ we
Scrap worldwide events from multiple categories (codes) from rsoe-edis.org.

Usage: we [OPTION]

'we' depends on its directory structure, so just use a symbolic
link if you want to have it in your PATH, do not move the executable alone.
subdirectories. Do not move the executable. Using a symlink is fine.

  Options:
    -g, --get [CODE]          Scrap data for event code to data/CODE.json.
    -p, --print [CODE]        Print saved data as json for event code.
    -t, --table [CODE]        Print saved data as table for event code.
    -l, --list-codes          List codes currently associated to scripts.
    -s, --setup               Create scrap scripts for each existing event code.
    -u, --update-codes        Fetch current event codes and save them.
    -R, --rm-scripts          Remove existing script(s) (clean scripts/ directory).
    -C, --clear-data ([CODE]) Remove queried data or all data files (clean data/ directory).
    -v, --version             Print program version and exit.
    -h, --help                Print this help.

  Improve me:
    https://git.teknik.io/matf/worldevents
```
#### Example for animal epidemic (code EPA):

```bash
$ we --list-codes
AAT	EPA	EPD	EPH	INH	HEC	LSC	PSI	SDM	TER	
EVP	PPP	IND	SUE	IBE	OUD	ERQ	LSL	VOE	FLD	
CBE	MIA	OHI	OTE	TRI	AIR	PRA	WTR	CYC	DRT	
EXR	HAI	HEW	LIT	PTF	SEW	STO	

$ we --get epa
Appended data to /home/user/Projects/worldevents/data/EPA.json. ✔

$ we --print epa
{
  "Date": [
    "2021-08-25 20:28:42",
    "2021-08-25 19:49:22",
    "2021-08-25 16:39:46"
  ],
  "Location": [
    "Benin, Africa",
    "Nigeria, Africa",
    "South Africa, Africa"
  ],
  "Title": [
    "Benin - Benin confirms H5N1 avian flu outbreak",
    "Nigeria - Nigeria's southern state reports bird flu outbreak",
    "South Africa - Khayelitsha animal clinic records two rabies cases after more than 20 years"
  ],
  "Details": [
    "https://rsoe-edis.org/eventList/details/111380/0",
    "https://rsoe-edis.org/eventList/details/111370/0",
    "https://rsoe-edis.org/eventList/details/111325/0"
  ]
}
```
```
###
# Not implemented yet
###
$ we --table epa
Date                 Title                                                                        Details
-------------------  ---------------------------------------------------------------------------  ------------------------------------------------
2021-08-25 20:28:42  Benin - Benin confirms H5N1 avian flu outbreak                               https://rsoe-edis.org/eventList/details/111380/0
2021-08-25 19:49:22  Nigeria - Nigeria's southern state reports bird flu outbreak                 https://rsoe-edis.org/eventList/details/111370/0
2021-08-25 16:39:46  South Africa - Khayelitsha animal clinic records two rabies cases after mor  https://rsoe-edis.org/eventList/details/111325/0
```

#### Clear existing data

```bash
$ we --clear-data air
Wrn: permanently delete AIR.json? This cannot be undone. [y/N] y
/home/user/Projects/worldevents/data/AIR.json removed. ✔

$ we --clear-data
Wrn: you are about to permanently delete 8 previously scraped data file(s). Are you sure? Type YES to confirm. YES
/home/user/Projects/worldevents/data/ directory cleaned. ✔

$ we --rm-scripts
Wrn: remove 37 scrap scripts? [y/N] y
/home/user/Projects/worldevents/scripts/ directory cleaned. ✔
Run 'we -s' to regenerate scrap scripts.
```

## To do
- [ ] Automate scrapping event codes into `setup/codes.txt`
- [ ] Add an option to scrap all categories at once instead of putting strain on the website with a request for every event category
- [ ] Implement `-t`
- [ ] Human readable categories, not only codes
- [ ] Better appending (avoid duplicates, add request date, merge into same json objects instead of creating new ones)
- [x] Make functions into a master script that would generate scripts, clear scripts,show data, delete data, and hopefully fetch codes in case of new categories available (latter part not done yet)

## Disclaimer
Credits to aetin. I was just reading about the `gemini` protocol and testing it with the cool `amfora` client, then stumbled upon `gemini://aetin.art/earth.gmi` and found the concept pretty cool, so I started playing with it. I am not a programmer, and I don't know how to write Python, so don't set your expectations too high.

This is merely a way for me to play with web-scraping and Python for something I find useful, but I am not responsible for what you may use this for. Please just don't abuse using the scrap scripts so that rsoe-edis.org doesn't start adding reCaptchas to their website.
