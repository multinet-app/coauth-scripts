#!/bin/sh
set -e

cyphershell=${CYPHERSHELL:-cypher-shell}
username=${USERNAME:-neo4j}
password=${PASSWORD:-neo4j}

out="$(mktemp -u)"

echo "call apoc.export.json.query(\"match (p) return p;\", \"${out}\");" | ${cyphershell} -u ${username} -p ${password}
echo ${out}
