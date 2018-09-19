import typing


class Validity(object):
    def __init__(self, messages: typing.Sequence[str]) -> None:
        self.messages = messages

    @classmethod
    def valid(cls) -> 'Validity':
        return cls(list())

    @classmethod
    def invalid(cls, msg: str, *msgs: str) -> 'Validity':
        return cls([msg] + list(msgs))

    def __str__(self) -> str:
        if self:
            return 'Validity.Valid'
        else:
            return 'Validity.Invalid<{0}>'.format(len(self.messages))

    def __bool__(self) -> bool:
        return not bool(self.messages)

    def __add__(self, other: typing.Any) -> 'Validity':
        if not isinstance(other, type(self)):
            return NotImplemented
        else:
            return Validity(
                list(self.messages) + list(other.messages)
            )
