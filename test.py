#!/usr/bin/env python

import bnf.demos.bnfparser as b
res = b.run()
print(res[1] == res[3])
print(res[1] == b.lang)
print(b.lt.validate(res[1]).messages)
