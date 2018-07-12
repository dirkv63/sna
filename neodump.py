"""
This script will extract information from Neo4J database and dump it in files that can be used for import into Neo4J.
"""

import logging
import os
from lib import my_env

cfg = my_env.init_env("neodump", __file__)
logging.info("Start Application")

# Get nodestore
db_dir = cfg["NeoDB"]["db_dir"]
neo_db = cfg["NeoDB"]["neo_db"]
nodestore = cfg["NeoDB"]["nodestore"]
nr_len = int(cfg["NeoDB"]["nr_len"])
nsfn = os.path.join(db_dir, neo_db, nodestore)
nsfh = open(nsfn, "rb")
nsf = nsfh.read()
max_nodes = len(nsf) // nr_len
# Collect node IDs
node_ids = []
# Todo - check that record on last position is included, or do I need range(max_nodes+1) - Test with index out of range
for pos in range(max_nodes):
    in_use = nsf[pos*nr_len]
    if in_use:
        node_ids.append(pos)
print("Number of nodes: {l}".format(l=len(node_ids)))
print("Nodes: \n{n}".format(n=node_ids[:15]))
logging.info("End Application")
