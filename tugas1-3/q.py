import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

mode = sys.argv[3] if len(sys.argv) > 3 else "captures"
query = Query(PY, pola)
cursor = QueryCursor(query)

if mode == "matches":
    for _, cap in cursor.matches(tree.root_node):
        nama = cap["nama"][0].text.decode() if "nama" in cap and cap["nama"] else "-"
        params = cap.get("params", [])
        jumlah = params[0].named_child_count if params else 0
        baris = cap["nama"][0].start_point[0] + 1 if "nama" in cap and cap["nama"] else 0
        print(f"fungsi: {nama} | params: {jumlah} | baris {baris}")
else:
    hasil = cursor.captures(tree.root_node)
    for nama, nodes in hasil.items():
        for n in nodes:
            print(f"@{nama}  baris {n.start_point[0] + 1}: {n.text.decode()}")

