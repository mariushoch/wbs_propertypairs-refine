# refine.py

Refine script for Wikidata entity [suggester data](https://github.com/wmde/wbs_propertypairs). This is a temporary workaround for the problems laid out at [phabricator T132839](https://phabricator.wikimedia.org/T132839), supposed to be replaced by a more robust suggestion algorithm at some point.

## Usage
```
usage: refine.py [-h] infile outfile

Refine wbs_propertypairs for Wikidata usage. See https://phabricator.wikimedia.org/T132839.

positional arguments:
  infile      Input file
  outfile     Output file

optional arguments:
  -h, --help  show this help message and exit
```

Can also be used directly with the gzip-ed wbs_propertypairs:

`zcat PATH/TO/wbs_propertypairs.csv.gz | python refine.py /dev/stdin out.csv`