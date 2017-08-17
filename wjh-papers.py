import json
import ads
from collections import OrderedDict

def get_reference_data(p):
    """Summarise the bibliographic data of an article from an ADS query
Returns dict of 'author' (list of strings), 'title' (string), and
'ref' (string giving journal, first page, and year).

    """
    data = {}
    try:
        data['author'] = p.author
    except:
        data['author'] = 'Anon'
    try:
        data['title'] = p.title
    except:
        data['title'] = 'Untitled'
    try:
        refstring = p.pub
    except:
        refstring = 'Unknown'
    try:
        refstring += f' {p.volume}, {p.page[0]}'
    except:
        pass
    try:
        refstring += f' ({p.year})'
    except:
        pass
    data['ref'] = refstring
    return data


datafile = 'wjh-papers.json'

myfields = ['author', 'first_author', 'year', 'bibcode', 'title',
            'citation', 'bibstem', 'bibgroup', 'pub', 'doi', 'volume', 'page',
            'year', 'property']

# Get all my papers from ADS 
mypapers = list(ads.SearchQuery(author="Henney, W. J.", rows=500, fl=myfields))

# Construct dict of all my refereed papers
data = {p.bibcode: get_reference_data(p)
        for p in mypapers
        if "REFEREED" in p.property}
# Sort with most recent first
data = OrderedDict(reversed(sorted(data.items(), key=lambda t: t[0])))
# Dump to JSON file
with open(datafile, 'w') as f:
    json.dump(data, f, indent=4)
