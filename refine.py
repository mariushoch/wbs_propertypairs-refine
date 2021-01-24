import argparse
import json
import urllib.request

parser = argparse.ArgumentParser(description='Refine wbs_propertypairs for Wikidata usage. See https://phabricator.wikimedia.org/T132839.')
parser.add_argument("infile", help="Input file")
parser.add_argument("outfile", help="Output file")

args = parser.parse_args()

datatype_cache={}
def get_datatype(property_id):
    if not property_id in datatype_cache:
        api_url='https://www.wikidata.org/w/api.php?action=wbgetentities&props=datatype&format=json&smaxage=86400&maxage=86400'
        with urllib.request.urlopen(api_url + '&ids=' + property_id) as result:
            data = json.loads(result.read().decode())
            if not 'entities' in data:
                datatype_cache[property_id] = 'missing'
            else:
                datatype_cache[property_id] = data['entities'][property_id]['datatype']
    return datatype_cache[property_id]

# Returns true if the given line should be omitted
def filter_line(line):
    fields=line.strip().split(',', 6)
    if len(fields) != 6:
        # No idea what this is, don't filter it
        return False
    pid1, qid1, pid2, count, probability, context = fields
    if qid1 == '':
        qid1 = -1
    pid1 = int(pid1)
    qid1 = int(qid1)
    pid2 = int(pid2)

    # Remove all external ids with context=item
    if context == 'item' and get_datatype('P' + str(pid1)) == 'external-id':
        return True
    # These are totally excluded (in context=item)
    if context == 'item' and pid1 in [17, 18, 276, 301, 373, 463, 495, 571, 641, 1344, 1448, 1476]:
        return True
    # Remove P31 qualifier suggestions for these
    if context == 'qualifier' and pid1 in [569, 570, 571, 576] and pid2 == 31:
        return True

    return False

with open(args.infile) as in_file:
    with open(args.outfile, 'w') as out_file:
        # First line is the heading
        line = in_file.readline()
        out_file.write(line)

        line = in_file.readline()
        while line:
            if not filter_line(line):
                out_file.write(line)
            line = in_file.readline()
