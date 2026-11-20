export default grammar({
  name: 'filter',
  word: $ => $.identifier,
  extras: $ => [/\s/],
  rules: {
    query: $ => $._expr,
    _expr: $ => choice($.comparison, $.and_expression, $.or_expression),
    and_expression: $ => prec.left(2,seq($._expr, 'and', $._expr)), 
    or_expression: $ => prec.left(1, seq($._expr, 'or', $._expr)),
    comparison: $ => seq(
      $.identifier,
      choice('=', '!=', '>', '<', '>=', '<='), 
      choice($.string, $.number)),
      identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
      string: $ => /"[^"]*"/,
      number: $ => /\d+/,
  }
});