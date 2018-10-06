import os

with open(
    os.path.join(
        os.path.dirname(__file__),
        'text.grammar'
    )
) as f:
    text = f.read()
