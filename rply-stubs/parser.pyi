from typing import Callable, Never

from rply.lexer import LexerStream
from rply.parsergenerator import LRTable
from rply.token import Token

class LRParser(object):
    lr_table: LRTable
    error_handler: Callable

    def __init__(self, lr_table: LRTable, error_handler: Callable): ...
    def parse(
        self, tokenizer: LexerStream, state: int | None = None
    ) -> Token | Never: ...
    def _reduce_production(
        self, t, symstack: list[Token], statestack: list[int], state: int | None
    ) -> int: ...
