import os

with open(
    os.path.join(
        os.path.dirname(__file__),
        'intermediate_text.grammar'
    )
) as f:
    intermediate_text = f.read()
