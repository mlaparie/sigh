#!/bin/bash
#
# Generate individual .py files for each "subList" code from rsoe.edis.org.
# To get all subList codes, go to the rsoe events list, edit page source, and
# find each "subList-" occurrence, they are appended with codes.
# Save codes in cats.txt, with one code per line.
# (Can be done easily with kakoune and `%ssubList-w<ret>y%<a-d><a-p>`.

while read -r code;
    do sed "s/replaceme/$code/g" generate-scripts/template.py > "$code.py";
    chmod +x "$code.py";
    printf "$code.py"; printf '\033[32;1m %s \033[0m\n' "✔" ;
done < generate-scripts/codes.txt
