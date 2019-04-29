# coauth-scripts
Scripts for processing the Coauth dataset

## Usage

To run these scripts requires setting up the original database in a Neo4j
instance, running specific Cypher queries to extract the data into a workable
format, then running the Python scripts in this repo to convert it into node and
edge CSV files suitable for [Multinet Girder](https://github.com/multinet-app/multinet-girder).

1. Download the Neo4j data dump: `curl -O -J
   https://data.kitware.com/api/v1/file/5cc709cf8d777f072b766fbf/download`.
2. Unpack the data: `tar xzvf data_dblp.tar.gz`.
3. Load the data into Neo4j: `sudo neo4j-admin load --from=data_dblp/databases/
   --force=true`.
4. Extract the node data: `CYPHERSHELL=cypher-shell USERNAME=neo4j
   PASSWORD=neo4j sh all-nodes.sh` (subtituting `CYPHERSHELL`, `USERNAME`, and
   `PASSWORD` for your local equivalents). _Note that the final line of output
   from this script will be the name of a temp file containing the extracted
   node data, called `DUMPFILE` in the following step._
5. Run the Python script to convert the dumped data to CSV files: `python
   cypher2cnode.py author.csv journal.csv conference.csv <${DUMPFILE}`. This
   will create files `author.csv`, `journal.csv`, and `conference.csv`
   containing node data of those types.
6. Extract the edge data and pipe it through the Python script to convert it to
   a CSV: `CYPHERSHELL=cypher-shell USERNAME=neo4j PASSWORD=neo4j sh all-links.sh | python cypher2edge.py author.csv journal.csv conference.csv \>edges.csv` (again substituting proper values for `CYPHERSHELL`, `USERNAME`,
   and `PASSWORD`). This will create file `edges.csv` containing edge data
   between the records in the three node data files.

After running these steps you will have four files: `author.csv` containing
author node data; `journal.csv` and `conference.csv` containing publication node
data; and `edges.csv` containing edge data linking publications to authors via
an "authored by" relation.
