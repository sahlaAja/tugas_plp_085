from __future__ import annotations

import re
import sys
from pathlib import Path
from tree_sitter import Language, Parser

import tree_sitter_filter as tsfilter

FILTER_LANGUAGE = Language(tsfilter.language())
IDENT_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_.]*$")


def _ident_text(node, source: bytes) -> str:
    name = source[node.start_byte : node.end_byte].decode("utf-8")
    if not IDENT_RE.match(name):
        raise ValueError(f"Identifier tidak valid: {name!r}")
    return name


def _value_param(node, source: bytes):
    raw = source[node.start_byte : node.end_byte].decode("utf-8")
    if node.type == "string":
        return raw[1:-1]
    if node.type == "number":
        return int(raw)
    if node.type == "boolean":
        return raw == "true"
    raise ValueError(f"Tipe nilai tidak didukung: {node.type}")


def build_where_clause(node, source: bytes, params: list) -> str:
    if node.type == "query":
        named_children = [c for c in node.children if c.is_named]
        if not named_children:
            return "1 = 1"
        return build_where_clause(named_children[0], source, params)

    if node.type == "parenthesized":
        inner = next(c for c in node.children if c.is_named)
        return f"({build_where_clause(inner, source, params)})"

    if node.type == "not_expression":
        operand = next(c for c in node.children if c.is_named)
        return f"NOT ({build_where_clause(operand, source, params)})"

    if node.type in ("and_expression", "or_expression"):
        op = "AND" if node.type == "and_expression" else "OR"
        left, right = [c for c in node.children if c.is_named]
        left_sql = build_where_clause(left, source, params)
        right_sql = build_where_clause(right, source, params)
        return f"{left_sql} {op} {right_sql}"

    if node.type == "comparison":
        named = [c for c in node.children if c.is_named]
        col_node, val_node = named[0], named[1]
        # Ambil teks operator literal di antara identifier dan nilai
        between_text = source[col_node.end_byte : val_node.start_byte].decode("utf-8").strip()
        allowed_ops = {"=", "!=", ">", "<", ">=", "<="}
        if between_text not in allowed_ops:
            raise ValueError(f"Operator perbandingan tidak didukung: {between_text!r}")
        col = _ident_text(col_node, source)
        params.append(_value_param(val_node, source))
        return f"{col} {between_text} ?"

    if node.type == "in_expression":
        named = [c for c in node.children if c.is_named]
        col = _ident_text(named[0], source)
        val_nodes = named[1:]
        placeholders = []
        for v in val_nodes:
            params.append(_value_param(v, source))
            placeholders.append("?")
        return f"{col} IN ({', '.join(placeholders)})"

    if node.type == "contains_expression":
        named = [c for c in node.children if c.is_named]
        col, val_node = named[0], named[1]
        col_name = _ident_text(col, source)
        val = _value_param(val_node, source)
        params.append(f"%{val}%")
        return f"{col_name} LIKE ?"

    if node.type == "ERROR":
        raise SyntaxError(f"Terdapat ERROR node pada posisi {node.start_point}..{node.end_point}")

    raise ValueError(f"Node AST tidak dikenali: {node.type}")


def parse_to_sql(query_text: str) -> tuple[str, list]:
    parser = Parser(FILTER_LANGUAGE)
    source = query_text.encode("utf-8")
    tree = parser.parse(source)
    params: list = []
    where_sql = build_where_clause(tree.root_node, source, params)
    return where_sql, params


if __name__ == "__main__":
    sample = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        'status in ("open", "pending", "closed") and title contains "invoice" and active = true'
    )
    sql_where, sql_params = parse_to_sql(sample)
    print("WHERE :", sql_where)
    print("PARAMS:", sql_params)