import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

try:
    import tree_sitter_javascript as tsjavascript
    HAS_JS = True
except ImportError:
    HAS_JS = False

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNC_PY = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")

SKIP_DIRS = {"venv", ".venv", ".git", "node_modules", "__pycache__"}

def nama_node(node):
    if node is None:
        return "<anonim>"
    return node.text.decode(errors="replace").strip()
def cari_node_error(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_node_error(child)
        if hasil is not None:
            return hasil
    return None

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME (sudah jadi)
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {nama_node(node)}")

    # Fitur 2 (TODO): fungsi yang lebih dari 30 baris
    for _, captures in QueryCursor(Q_FUNC_PY).matches(tree.root_node):
        daftar_nama = captures.get("nama", [])
        daftar_fungsi = captures.get("fungsi", [])
        nama_fn = nama_node(daftar_nama[0]) if daftar_nama else "<anonim>"
        for fn in daftar_fungsi:
            jumlah_baris = fn.end_point[0] - fn.start_point[0] + 1
            if jumlah_baris > 30:
                print(
                    f"{path}:{fn.start_point[0] + 1}: fungsi '{nama_fn}' "
                    f"panjangnya {jumlah_baris} baris (> 30)"
                )
    # Fitur 3 (TODO): file yang pohonnya mengandung error
    if tree.root_node.has_error:
        err_node = cari_node_error(tree.root_node)
        baris_err = (err_node.start_point[0] + 1) if err_node else (tree.root_node.start_point[0] + 1)
        jenis = "MISSING" if (err_node and err_node.is_missing) else "ERROR"
        print(f"{path}:{baris_err}: terdapat syntax {jenis}")

for path in Path(sys.argv[1]).rglob("*.py"):
    if any(part in SKIP_DIRS for part in path.parts):
        continue
    cek_file(path)

