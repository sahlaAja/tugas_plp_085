; Kata kunci
[
  "and"
  "or"
  "not"
  "in"
  "contains"
] @keyword

; Operator perbandingan
[
  "="
  "!="
  ">"
  "<"
  ">="
  "<="
] @operator

; Tanda kurung & koma (opsional)
[
  "("
  ")"
  ","
] @punctuation.bracket

; Nilai literal
(string) @string
(number) @number
(boolean) @boolean

; Nama field (identifier)
(comparison
  (identifier) @property)

(in_expression
  (identifier) @property)

(contains_expression
  (identifier) @property)

(identifier) @variable
