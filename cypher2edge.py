import csv
import pprint
import sys
import uuid


def lookup_table(filename, field1, field2):
    table = {}
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            table[row[field1]] = row[field2]

    return table


def strip(string):
    return string[2:-1]


def main():
    if len(sys.argv) < 4:
        print('usage: cypher2node.py <authorcsv> <journalcsv> <confcsv>', file=sys.stderr)
        return 1

    authorcsv = sys.argv[1]
    journalcsv = sys.argv[2]
    confcsv = sys.argv[3]

    # Create lookup tables mapping from name/title to key.
    author_table = lookup_table(authorcsv, 'name', '_key')
    journal_table = lookup_table(journalcsv, 'title', '_key')
    conf_table = lookup_table(confcsv, 'title', '_key')

    # Iterate through the data on sys.stdin, creating edge table records from
    # the names in the line and the lookup tables.
    reader = csv.DictReader(sys.stdin)
    edges = []
    for row in reader:
        # Find the author node.
        #
        # NOTE: the space before "author" is intentional, due to the way
        # cypher-shell generates CSV-style results.
        author_key = None
        author = strip(row[' author'])
        try:
            author_key = author_table[author]
        except KeyError:
            print('fatal error: missing author "{}"'.format(author))
            pprint.pprint(row)

        # Find the publication node.
        pub_key = None
        pub_type = None
        try:
            pub_key = journal_table[row['title']]
            pub_type = 'journal'
        except KeyError:
            try:
                pub_key = conf_table[row['title']]
                pub_type = 'conference'
            except KeyError:
                print('fatal error: missing publication "{}"'.format(row['title']))
                pprint.pprint(row)

        edges.append({'_from': '{}/{}'.format(pub_type, pub_key),
                      '_to': 'author/{}'.format(author_key),
                      '_key': str(uuid.uuid4())})

    # Write the edgefile to CSV.
    writer = csv.DictWriter(sys.stdout, ['_key', '_from', '_to'])
    writer.writeheader()
    writer.writerows(edges)


if __name__ == '__main__':
    sys.exit(main())
