from .parser import lang
from .transform import lt

def run():
    with open('bnf.bnf') as f:
        bnf_plaintext = f.read()

    tree = lang.parse(bnf_plaintext)
    result = lt.transform(tree)

    tree2 = result.parse(bnf_plaintext)
    result2 = lt.transform(tree2)

    return (tree, result, tree2, result2)
