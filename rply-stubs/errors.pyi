from rply.token import SourcePosition


class ParserGeneratorError(Exception):
    pass


class LexingError(Exception):
    message: str
    source_pos: SourcePosition

    def __init__(self, message: str, source_pos: SourcePosition):
        ...

    def getsourcepos(self) -> SourcePosition:
        ...

    def __repr__(self) -> str:
        ...


class ParsingError(Exception):
    message: str
    source_pos: SourcePosition

    def __init__(self, message: str, source_pos: SourcePosition):
        ...

    def getsourcepos(self) -> SourcePosition:
        ...

    def __repr__(self) -> str:
        ...

class ParserGeneratorWarning(Warning):
    pass