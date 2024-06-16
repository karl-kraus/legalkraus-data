from acdh_tei_pyutils.tei import TeiReader


file = "./data/indices/listlegal.xml"
doc = TeiReader(file)
for i, x in enumerate(doc.any_xpath(".//tei:bibl"), start=1):
    xml_id = f"legal-{i:03}"
    x.attrib["{http://www.w3.org/XML/1998/namespace}id"] = xml_id
doc.tree_to_file(file)
