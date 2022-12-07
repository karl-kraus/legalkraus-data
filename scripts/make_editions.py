import glob
import os
import shutil
import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm

from config import OBJ_DIR

editions = "../editions"

print(f"converts files from {OBJ_DIR} into better TEIs and saves them into {editions}")
print(f'adds proper "ref" values to fackel references')
print("removes schema references and attributes from TEI header")

list_fackel = TeiReader("../indices/listfackel.xml")
d = {}
for x in list_fackel.any_xpath(".//tei:bibl/tei:ref"):
    target = x.attrib["target"]
    bibl = x.getparent()
    bibl_id = bibl.attrib["{http://www.w3.org/XML/1998/namespace}id"]
    d[target] = bibl_id

files = sorted(glob.glob(f"{OBJ_DIR}/D_*.xml"))
editions = "../editions"
shutil.rmtree(editions)
os.makedirs(editions, exist_ok=True)
tei_head = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://raw.githubusercontent.com/acdh-oeaw/legalkraus-documentation/master/odd/legalkraus_transcr.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="https://raw.githubusercontent.com/acdh-oeaw/legalkraus-documentation/master/schematron/legalkraus_transcr.sch" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"
"""

for x in tqdm(files, total=len(files)):
    _, tail = os.path.split(x)
    with open(x, "r") as f:
        data = f.read()
    data = data.replace(tei_head, '<TEI xmlns="http://www.tei-c.org/ns/1.0"')
    for key, value in d.items():
        to_find = f'ref="{key}"'
        to_replace = f'ref="#{value}" corresp="{key}"'
        data = data.replace(to_find, to_replace)

    out_file = os.path.join(editions, tail)
    with open(out_file, "w") as fp:
        fp.write(data)

print("removes all attributes from tei:TEI")

files = sorted(glob.glob(f"{editions}/*.xml"))
for x in tqdm(files, total=len(files)):
    doc = TeiReader(x)
    root = doc.any_xpath('/tei:TEI')[0]
    for key, value in root.attrib.items():
        root.attrib.pop(key)
    doc.tree_to_file(x)
