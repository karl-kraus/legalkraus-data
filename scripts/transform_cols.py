import json
import glob
import os
import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader

from config import COL_DIR, ABSTRACTS, TMP_DIR

with open(ABSTRACTS, "r") as f:
    data = json.load(f)

files = sorted(glob.glob(f"{COL_DIR}/*.xml"))

counter = 1
for x in files:
    try:
        abstract_data = data[f"{counter}"]
    except KeyError:
        abstract_data = f"Kein Informationen vorhanden für Fall-ID: {counter}"
    counter += 1
    _, tail = os.path.split(x)
    doc = TeiReader(x)
    file_desc = doc.any_xpath(".//tei:fileDesc")[0]
    list_org = doc.any_xpath(".//tei:listOrg")[0]
    partic_desc = doc.any_xpath(".//tei:particDesc")[0]
    text_class = doc.any_xpath(".//tei:textClass")[0]
    partic_desc.append(list_org)
    profile_desc = ET.Element("{http://www.tei-c.org/ns/1.0}profileDesc")
    ab = ET.Element("{http://www.tei-c.org/ns/1.0}abstract")
    p = ET.Element("{http://www.tei-c.org/ns/1.0}p")
    p.text = abstract_data
    ab.append(p)
    profile_desc.append(ab)
    profile_desc.append(text_class)
    profile_desc.append(partic_desc)
    file_desc.addnext(profile_desc)
    try:
        doc.any_xpath(".//tei:listPerson/tei:person")[0]
    except IndexError:
        for bad in doc.any_xpath(".//tei:listPerson"):
            bad.getparent().remove(bad)
    try:
        doc.any_xpath(".//tei:listOrg/tei:org")[0]
    except IndexError:
        for bad in doc.any_xpath(".//tei:listOrg"):
            bad.getparent().remove(bad)
    for ab in doc.any_xpath(".//tei:ab"):
        ab.tag = "{http://www.tei-c.org/ns/1.0}note"
    try:
        doc.any_xpath(".//tei:particDesc/*")[0]
    except:
        for bad in doc.any_xpath(".//tei:particDesc"):
            bad.getparent().remove(bad)
    for ref in doc.any_xpath(".//tei:*[@ref]"):
        ref.attrib["sameAs"] = ref.attrib.pop("ref")
    doc.tree_to_file(f"{os.path.join(TMP_DIR, tail)}")
