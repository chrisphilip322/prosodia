bnf = r"""<Syntax> ::= <Rules> <EOF>
<Rules> ::= <Rule> | <Rule> <Rules>
<Rule> ::= <OptWhitespace> "<" <RuleName> ">" <OptWhitespace> "::=" <OptWhitespace> <Expression> <LineEnd>
<OptWhitespace> ::= " " <OptWhitespace> | ""
<Expression> ::= <List> | <List> <OptWhitespace> "|" <OptWhitespace> <Expression>
<LineEnd> ::= <SingleLineEnd> | <SingleLineEnd> <LineEnd>
<SingleLineEnd> ::= <OptWhitespace> <EOL>
<List> ::= <Term> | <Term> <OptWhitespace> <List>
<Term> ::= <Literal> | "<" <RuleName> ">"
<Literal> ::= '"' <Text1> '"' | "'" <Text2> "'"
<Text1> ::= "" | <Character1> <Text1>
<Text2> ::= "" | <Character2> <Text2>
<Character> ::= <Letter> | <Digit> | <Symbol>
<Letter> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
<Digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<Symbol> ::= "|" | " " | "!" | "#" | "$" | "%" | "&" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | ">" | "=" | "<" | "?" | "@" | "[" | "\" | "]" | "^" | "_" | "`" | "{" | "}" | "~"
<Character1> ::= <Character> | "'"
<Character2> ::= <Character> | '"'
<RuleName> ::= <Letter> | <Letter> <RuleEnd>
<RuleEnd> ::= <OneRuleEnd> | <OneRuleEnd> <RuleEnd>
<OneRuleEnd> ::= <Letter> | <Digit> | "-" <Letter> | "-" <Digit>
"""
