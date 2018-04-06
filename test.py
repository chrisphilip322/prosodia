#!/usr/bin/env python

import bnf.demos.bnfparser as b
res = b.run()
print(res[1] == res[3])
print(res[1] == b.lang)
validity = res[1].validate()
for m in validity.messages:
    print(m)
if validity:
    print('language is valid')
validity = b.lt.validate(res[1])
for m in validity.messages:
    print(m)
if validity:
    print('language transform is valid')
