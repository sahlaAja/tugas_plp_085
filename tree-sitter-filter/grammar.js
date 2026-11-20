export default grammar({
  name: 'filter',
  word: $ => $.identifier,
  extras: $ => [/\s/],
  rules: {
    query: $ => $._expr,
    _expr: $ => choice($.comparison, $.in_expression,
      $.contains_expression, $.and_expression, $.or_expression, $.not_expression, $.parenthesized),
      _value: $ => choice(
        $.string,
        $.number,
        $.boolean
      ),
      in_expression: $ => seq(
        $.identifier,
        'in',
        '(',
        $._value,
        repeat(seq(',', $._value)),
        ')'
      ),
      contains_expression: $ => seq(
        $.identifier,
        'contains',
        $._value
      ),
    not_expression: $ => prec.right(3, seq('not', $._expr)),
    and_expression: $ => prec.left(2,seq($._expr, 'and', $._expr)), 
    or_expression: $ => prec.left(1, seq($._expr, 'or', $._expr)),
    parenthesized: $ => seq('(', $._expr, ')'),
    comparison: $ => seq(
      $.identifier,
      choice('=', '!=', '>', '<', '>=', '<='), 
      $._value),
      identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
      string: $ => /"[^"]*"/,
      number: $ => /\d+/,
      boolean: $ => choice('true', 'false'),
  }
});