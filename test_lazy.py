#!/usr/bin/env python

import parser_v2 as p

def square(x: str) -> int:
    print('squaring', x)
    return int(x) ** 2

x = p.LazySequenceTransform(
    [
        p.LiteralNode("5"),
        p.LiteralNode("6"),
        p.LiteralNode("7"),
    ],
    [
        square,
        square,
        square
    ],
    None
)
print(x[0])
