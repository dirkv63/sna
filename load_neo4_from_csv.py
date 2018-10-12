"""
This script will create and execute the command line to load nodes and relationships in the Neo4J database.
Node files need to start with node_, then have an identier (node label), then have a counter. First file must be the
header line. Subsequent files are data files.
Relation files need to start with rel_, then have an identifier (relation label), then have a counter. First file
must be the header line. Subsequent files are data files.
"""

import logging
import os
import subprocess as sp
from lib import my_env

cfg = my_env.init_env("sna", __file__)
logging.info("Start Application")

cmd = os.path.join(cfg["Graph"]["path"], cfg["Graph"]["adm"])
args = [cmd, "import", "--database={db}".format(db=cfg["Graph"]["db"])]

os.listdir()

nodes.append("params")
nodes.append("applications")
for lbl in nodes:
    hdr = os.path.join(cfg["Main"]["neo4jcsv_dir"], "node_{lbl}_1.csv".format(lbl=lbl))
    con = os.path.join(cfg["Main"]["neo4jcsv_dir"], "node_{lbl}_2.csv".format(lbl=lbl))
    arg = "--nodes={hdr},{con}".format(hdr=hdr, con=con)
    args.append(arg)

rf = os.path.join(cfg["Main"]["neo4jcsv_dir"], "relations.csv")
arg = "--relationships={rf}".format(rf=rf)
args.append(arg)
module = my_env.get_modulename(__file__)
sof = os.path.join(cfg["Main"]["logdir"], "{mod}_out.log".format(mod=module))
sef = os.path.join(cfg["Main"]["logdir"], "{mod}_err.log".format(mod=module))
# print(" ".join(args))
so = open(sof, "w")
se = open(sef, "w")
try:
    sp.run(args, stderr=se, stdout=so, check=True)
except sp.CalledProcessError as e:
    logging.error("Some issues during execution, check {sef} and {sof}".format(sof=sof, sef=sef))
else:
    logging.info("No error messages returned, see {sof}!".format(sof=sof))
se.close()
so.close()
