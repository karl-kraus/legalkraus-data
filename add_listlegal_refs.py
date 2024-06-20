import glob
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from tqdm import tqdm

print("adds proper ref values to rs type='legal'")
print("see https://github.com/karl-kraus/legalkraus-data/issues/4")

file = "./data/indices/listlegal.xml"
doc = TeiReader(file)

lookup_dict = {}
for i, x in enumerate(doc.any_xpath(".//tei:bibl"), start=1):
    xml_id = get_xmlid(x)
    try:
        corresp = x.attrib["corresp"]
    except KeyError:
        lookup_dict["nicht-identifziert"] = "legal-nicht-identifiziert"
        continue
    lookup_dict[corresp] = xml_id


for x in tqdm(glob.glob("./data/editions/*xml")):
    doc = TeiReader(x)
    for y in doc.any_xpath(".//tei:rs[@type='law' and @ref]"):
        corresp = y.attrib["ref"]
        if corresp:
            try:
                new_ref = lookup_dict[corresp]
            except KeyError:
                new_ref = lookup_dict["nicht-identifziert"]
        else:
            corresp = "nicht-identifziert"
            new_ref = lookup_dict["nicht-identifziert"]
        y.attrib["ref"] = f"#{new_ref}"
        y.attrib["corresp"] = corresp
    doc.tree_to_file(x)
