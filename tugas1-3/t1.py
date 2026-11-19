import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode_list = [
    b"def sapa(nama):\n    return nama\n",
    b"if x > 0:\n    y = 1\nelse:\n    y = 0\n",
    b"class Akun:\n    def saldo(self):\n        return 0\n",
]

for syn in kode_list:
  tree = parser.parse(syn)
  print("Kode:")
  print(syn.decode())
  print("Pohon (eksekusi):")
  print(tree.root_node)
  print("-" * 50)

# Langkah 5: Cek node bernama vs anonim pada potongan fungsi & isi parameters
tree_fungsi = parser.parse(kode_list[0])
func_node = tree_fungsi.root_node.children[0]

print("=== Anak langsung dari function_definition ===")
for c in func_node.children:
  print(c.type, "bernama" if c.is_named else "anonim")
  if c.type == "parameters":
    for p in c.children:
      print("  ->", p.type, "bernama" if p.is_named else "anonim")

# Langkah 6: Rusak kode dengan sengaja (hapus ':' setelah def sapa(nama))
kode_rusak = b"def sapa(nama)\n    return nama\n"
tree_rusak = parser.parse(kode_rusak)

print("\n=== Kode rusak (tanpa ':') ===")
print(tree_rusak.root_node)