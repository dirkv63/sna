"""
This script will convert the russians.net pajek file into nodes and relations file for import in Neo4J.
"""

import logging
import networkx
import os
from lib import my_env

cfg = my_env.init_env("sna", __file__)
logging.info("Start Application")
data_dir = cfg["Data"]["dir"]
rfn = cfg["Data"]["russians"]
rf = os.path.join(data_dir, rfn)
logging.info("Read network")
g = networkx.read_pajek(rf)

li = my_env.LoopInfo("Nodes", 1000)
nodes = "name:ID{delim}:LABEL\n".format(delim=my_env.delim)
for node in g.nodes():
    li.info_loop()
    nodes += '"{node}"{delim}Person\n'.format(node=node, delim=my_env.delim)
li.end_loop()

li = my_env.LoopInfo("Relations", 1000)
rels = ":START_ID{delim}:END_ID{delim}:TYPE\n".format(delim=my_env.delim)
for rel in g.edges():
    li.info_loop()
    (sn, en) = rel
    rels += '"{sn}"{delim}"{en}"{delim}contacts\n'.format(delim=my_env.delim, sn=sn, en=en)
li.end_loop()

import_dir = cfg["Graph"]["import_dir"]
nf = os.path.join(import_dir, "persons.csv")
rf = os.path.join(import_dir, "contacts.csv")

nfh = open(nf, "w")
nfh.write(nodes)
nfh.close()

rfh = open(rf, "w")
rfh.write(rels)
rfh.close()
