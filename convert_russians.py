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

# Remove all files in import dir
import_dir = cfg["Graph"]["import_dir"]
file_list = os.listdir(import_dir)
for file in file_list:
    os.remove(os.path.join(import_dir, file))

# First write header lines
nf = os.path.join(import_dir, "node_persons_1.csv")
rf = os.path.join(import_dir, "rel_contacts_1.csv")
nhl = "name:ID{delim}:LABEL".format(delim=my_env.delim)
rhl = ":START_ID{delim}:END_ID{delim}:TYPE".format(delim=my_env.delim)

nfh = open(nf, "w")
nfh.write(nhl)
nfh.close()

rfh = open(rf, "w")
rfh.write(rhl)
rfh.close()

li = my_env.LoopInfo("Nodes", 1000)
nodes = ""
for node in g.nodes():
    li.info_loop()
    nodes += '"{node}"{delim}Person\n'.format(node=node, delim=my_env.delim)
li.end_loop()

li = my_env.LoopInfo("Relations", 1000)
rels = ""
for rel in g.edges():
    li.info_loop()
    (sn, en) = rel
    rels += '"{sn}"{delim}"{en}"{delim}contacts\n'.format(delim=my_env.delim, sn=sn, en=en)
li.end_loop()

nf = os.path.join(import_dir, "node_persons_2.csv")
rf = os.path.join(import_dir, "rel_contacts_2.csv")

nfh = open(nf, "w")
nfh.write(nodes)
nfh.close()

rfh = open(rf, "w")
rfh.write(rels)
rfh.close()
