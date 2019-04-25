#!/bin/sh

cypher-shell "match (a)-[]->(b) return a.title,b.name;" --format plain
