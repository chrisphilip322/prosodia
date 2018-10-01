import os

with open(
    os.path.join(
        os.path.dirname(__file__),
        'group_text.grammar'
    )
) as f:
    example_group_augmentedbnf_text = f.read()
