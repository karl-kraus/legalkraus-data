import glob
import re
from acdh_tei_pyutils.tei import TeiReader

print("check for missing pmb prefixes before pmb-ids and adds the prefix")

files = glob.glob("./data/editions/*.xml")
pattern = r"#\d+"
regex = re.compile(pattern)

ids = set()
for x in files:
    doc = TeiReader(x)
    for elem in doc.tree.iter():
        for attr, value in elem.attrib.items():
            if regex.match(value):
                new_value = f"#pmb{value[1:]}"
                print(value, new_value)
                elem.attrib[attr] = new_value
    doc.tree_to_file(x)