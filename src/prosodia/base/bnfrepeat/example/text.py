bnfrepeattext = r"""<Syntax> ::= <Rule>{1,} <EOF>
<Rule> ::= <OptWhitespace> "<" <RuleName> ">" <OptWhitespace> "::=" <OptWhitespace> <Expression> <SingleLineEnd>{1,}
<OptWhitespace> ::= " "{0,}
<Expression> ::= <List> <ExpressionEnd>{0,}
<ExpressionEnd> ::= <OptWhitespace> "|" <OptWhitespace> <List>
<SingleLineEnd> ::= <OptWhitespace> <EOL>
<List> ::= <Term> <ListEnd>{0,}
<ListEnd> ::= <OptWhitespace> <Term>
<Term> ::= <BaseTerm> | <BaseTerm> "{" <RepeatBody> "}"
<RepeatBody> ::= <Number> | <Number> "," | <Number> "," <Number>
<BaseTerm> ::= <Literal> | "<" <RuleName> ">" | <LiteralRange>
<Literal> ::= '"' <Text1> '"' | "'" <Text2> "'"
<Text1> ::= <Character1>{0,}
<Text2> ::= <Character2>{0,}
<Character> ::= <Letter> | <Digit> | <Symbol>
<Letter> ::= /65-90/ | /97-122/
<Digit> ::= "0" | <NonZeroDigit>
<NonZeroDigit> ::= /49-57/
<Symbol> ::= /32-33/ | /35-38/ | /40-47/ | /58-64/ | /91-96/ | /123-126/
<Character1> ::= <Character> | "'"
<Character2> ::= <Character> | '"'
<RuleName> ::= <Letter> <OneRuleEnd>{0,}
<OneRuleEnd> ::= <Letter> | <Digit> | "-" <Letter> | "-" <Digit>
<LiteralRange> ::= "/" <Number> "/" | "/" <Number> "-" <Number> "/"
<Number> ::= <Digit> | <NonZeroDigit> <Digit>{1,}
"""
