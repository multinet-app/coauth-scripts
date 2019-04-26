#!/bin/sh
set -e

cyphershell=${CYPHERSHELL:-cypher-shell}
username=${USERNAME:-neo4j}
password=${PASSWORD:-neo4j}

${cyphershell} "match (a)-[]->(b) return a.title as title,b.name as author;" -u ${username} -p ${password} --format plain
