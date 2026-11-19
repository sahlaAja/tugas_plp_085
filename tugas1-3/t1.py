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