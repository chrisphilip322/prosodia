from .text import bnf as bnf_plaintext
from .parser import lang
from .transform import lt

def run():
    tree = lang.parse(bnf_plaintext)
    result = lt.transform(tree)

    tree2 = result.parse(bnf_plaintext)
    result2 = lt.transform(tree2)

    return (tree, result, tree2, result2)
