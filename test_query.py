from tree_sitter import Language, Parser, Query, QueryCursor
import tree_sitter_filter as tsfilter

FILTER_LANGUAGE = Language(tsfilter.language())
parser = Parser(FILTER_LANGUAGE)

teks = b'status = "open" and (priority > 2 or owner = "budi")'
tree = parser.parse(teks)

query = Query(
    FILTER_LANGUAGE,
    """
    (comparison
      field: (identifier) @field
      value: (_) @value)
    """,
)

cursor = QueryCursor(query)
captures = cursor.captures(tree.root_node)

for nama_tag, daftar_node in captures.items():
  for node in daftar_node:
    potongan = teks[node.start_byte : node.end_byte].decode("utf-8")
    print(f"@{nama_tag} -> {potongan} [{node.type}]")