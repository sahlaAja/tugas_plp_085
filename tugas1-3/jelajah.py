import sys
from pathlib import Path 
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    # TODO: untuk setiap child yang bernama, panggil jelajah() lagi
    #       dengan kedalaman + 1 dan nama field-nya.
    for i, child in enumerate(node.children):
        if child.is_named:
            nama_field = node.field_name_for_child(i)
            jelajah(child, kedalaman + 1, nama_field)

def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python tugas1-3\\jelajah.py <path_file.py>")
        sys.exit(1)
    
    target = Path(sys.argv[1])
    sumber = target.read_bytes()
    jumlah_baris = len(sumber.splitlines())
    if jumlah_baris < 100:
        print(f"# Catatan: {target} memiliki {jumlah_baris} baris (< 100 baris)")

    tree = parser.parse(sumber)
    jelajah(tree.root_node)

if __name__ == "__main__":
  main()