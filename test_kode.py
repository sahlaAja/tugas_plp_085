from tree_sitter import Language, Parser, Query, QueryCursor
import tree_sitter_python as tspython

PY = Language(tspython.language())
parser = Parser(PY)

src = b"""
def tambah(a, b):
    return a + b

def kali(a, b):
    print(a, b)
    return a * b
"""
tree = parser.parse(src)

print("=== Cara 1: Rekursi ===")


def cari_fungsi(node):
  if node.type == "function_definition":
    nama = node.child_by_field_name("name")
    print(nama.text.decode(), "baris", node.start_point[0] + 1)
  for child in node.named_children:
    cari_fungsi(child)


cari_fungsi(tree.root_node)

print("\n=== Cara 2: Query ===")
query = Query(PY, "(function_definition name: (identifier) @nama)")
captures = QueryCursor(query).captures(tree.root_node)
for node in captures["nama"]:
  print(node.text.decode())

print("\n=== Pengayaan: TreeCursor ===")
cursor = tree.walk()


def jalan_cursor(cur):
  while True:
    node = cur.node
    if node.type == "function_definition":
      print("Ditemukan fungsi via cursor:", node.child_by_field_name("name").text.decode())
    if cur.goto_first_child():
      jalan_cursor(cur)
      cur.goto_parent()
    if not cur.goto_next_sibling():
      break


jalan_cursor(cursor)

print("\n=== Pengayaan: Edit Inkremental ===")
# Cari posisi byte dan (baris, kolom) akurat untuk "tambah"
idx = src.find(b"tambah")
baris = src[:idx].count(b"\n")
awal_baris = src.rfind(b"\n", 0, idx)
kolom_awal = idx if awal_baris == -1 else idx - awal_baris - 1
kolom_akhir = kolom_awal + len(b"tambah")

new_src = src.replace(b"tambah", b"jumlah", 1)
tree.edit(
    start_byte=idx,
    old_end_byte=idx + len(b"tambah"),
    new_end_byte=idx + len(b"jumlah"),
    start_point=(baris, kolom_awal),
    old_end_point=(baris, kolom_akhir),
    new_end_point=(baris, kolom_awal + len(b"jumlah")),
)
new_tree = parser.parse(new_src, tree)
fresh_tree = parser.parse(new_src)

for r in tree.changed_ranges(new_tree):
  print("Rentang berubah:", r.start_point, "->", r.end_point)

print(
    "Sama dengan parse dari nol:",
    str(new_tree.root_node) == str(fresh_tree.root_node),
)