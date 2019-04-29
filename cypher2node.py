import csv
import json
import pprint
import unidecode
import sys


def write_csv(filename, fields, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(fields)
        for record in data:
            writer.writerow(map(lambda x: record[x], fields))


def main():
    if len(sys.argv) < 4:
        print('usage: cypher2csv.py <authorfile> <journalfile> <conffile>', file=sys.stderr)
        return 1

    authorfile = sys.argv[1]
    journalfile = sys.argv[2]
    conffile = sys.argv[3]

    # Create buckets for author nodes and publication nodes.
    authors = []
    conf_pubs = []
    journal_pubs = []

    # The input consists of a JSON string per line.
    author_key = set()
    for line in sys.stdin:
        rec = json.loads(line)['p']
        out = {}

        # Sweep through the labels field, looking for either "Article" or
        # "Author".
        label = None
        for label in rec['labels']:
            if label in ['Author', 'Article', 'ConferencePaper']:
                break

        # Split paths to handle authors and pubs differently.
        if label == 'Author':
            out['type'] = 'author'

            # Copy over properties.
            try:
                out['name'] = rec['properties']['name']
                out['_key'] = unidecode.unidecode(rec['properties']['id'])
            except KeyError as e:
                print(e)
                pprint.pprint(rec)

            # Disambiguate author keys if they wind up equal to something
            # already seen (this can happen if the author appears twice, once
            # with diacritics and once without).
            suffix = 0
            key = out['_key']
            while key in author_key:
                suffix += 1
                key = out['_key'] + str(suffix)
            out['_key'] = key

            author_key.add(out['_key'])
            authors.append(out)

        elif label == 'ConferencePaper':
            out['type'] = 'conference_publication'

            # Copy over properties.
            try:
                for field in ['year', 'booktitle', 'title', 'url']:
                    out[field] = rec['properties'][field]
            except KeyError as e:
                print(e)
                pprint.pprint(rec)

            # Set venue and key.
            key_parts = rec['properties']['key'].split('/')
            out['venue'] = key_parts[1]
            out['_key'] = '{}-{}'.format(key_parts[1], key_parts[2])

            conf_pubs.append(out)

        elif label == 'Article':
            out['type'] = 'journal_publication'

            # Copy over properties.
            try:
                for field in ['ee', 'year', 'title', 'url']:
                    out[field] = rec['properties'][field]
            except KeyError as e:
                print(e)
                pprint.pprint(rec)

            out['pages'] = rec['properties'].get('pages', 'unknown')

            # Set journal and key.
            key_parts = rec['properties']['key'].split('/')
            out['journal'] = key_parts[1]
            out['_key'] = '{}-{}'.format(key_parts[1], key_parts[2])

            journal_pubs.append(out)

        else:
            print('error: unknown node type {}'.format(rec['labels']))
            pprint.pprint(rec)

    write_csv(authorfile, ['_key', 'type', 'name'], authors)
    write_csv(conffile, ['_key', 'type', 'venue', 'year', 'booktitle', 'title', 'url'], conf_pubs)
    write_csv(journalfile, ['_key', 'type', 'journal', 'ee', 'year', 'title', 'url'], journal_pubs)


if __name__ == '__main__':
    sys.exit(main())
