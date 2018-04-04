#!/usr/bin/env python

from parse_bnf import tree
from test_transform import lt

result = lt.transform(tree)
with open('bnf.bnf') as f:
    bnf = f.read()

tree2 = result.parse(bnf)
result2 = lt.transform(tree2)
print(result == result2)
