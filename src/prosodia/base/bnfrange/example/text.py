example_bnfrangetext = r"""<Syntax> ::= <Rules> <EOF>
<Rules> ::= <Rule> | <Rule> <Rules>
<Rule> ::= <OptWhitespace> "<" <RuleName> ">" <OptWhitespace> "::=" <OptWhitespace> <Expression> <LineEnd>
<OptWhitespace> ::= " " <OptWhitespace> | ""
<Expression> ::= <List> | <List> <OptWhitespace> "|" <OptWhitespace> <Expression>
<LineEnd> ::= <SingleLineEnd> | <SingleLineEnd> <LineEnd>
<SingleLineEnd> ::= <OptWhitespace> <EOL>
<List> ::= <Term> | <Term> <OptWhitespace> <List>
<Term> ::= <Literal> | "<" <RuleName> ">" | <LiteralRange>
<Literal> ::= '"' <Text1> '"' | "'" <Text2> "'"
<Text1> ::= "" | <Character1> <Text1>
<Text2> ::= "" | <Character2> <Text2>
<Character> ::= <Letter> | <Digit> | <Symbol>
<Letter> ::= /65-90/ | /97-122/
<Digit> ::= "0" | <NonZeroDigit>
<NonZeroDigit> ::= /49-57/
<Symbol> ::= /32-33/ | /35-38/ | /40-47/ | /58-64/ | /91-96/ | /123-126/
<Character1> ::= <Character> | "'"
<Character2> ::= <Character> | '"'
<RuleName> ::= <Letter> | <Letter> <RuleEnd>
<RuleEnd> ::= <OneRuleEnd> | <OneRuleEnd> <RuleEnd>
<OneRuleEnd> ::= <Letter> | <Digit> | "-" <Letter> | "-" <Digit>
<LiteralRange> ::= "/" <Number> "/" | "/" <Number> "-" <Number> "/"
<Number> ::= <NonZeroDigit> | <NonZeroDigit> <Digits>
<Digits> ::= <Digit> | <Digit> <Digits>
"""
