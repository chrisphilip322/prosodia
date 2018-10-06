from prosodia.core.grammar import Grammar


def validate(test_case, validity):
    for msg in validity.messages:
        print(msg)
    test_case.assertTrue(validity)


def validate_recursive_grammar(test_case, grammar, text):
    validate(test_case, grammar.validate())

    parsed_lang = grammar.apply(text)
    parsed_grammar = Grammar(parsed_lang, grammar.transform)
    validate(test_case, parsed_lang.equals(grammar.language))
    validate(test_case, parsed_grammar.validate())

    parsed_lang2 = parsed_grammar.apply(text)
    parsed_grammar2 = Grammar(parsed_lang2, grammar.transform)
    validate(test_case, parsed_lang2.equals(grammar.language))
    validate(test_case, parsed_lang2.equals(parsed_lang))
    validate(test_case, parsed_grammar2.validate())
