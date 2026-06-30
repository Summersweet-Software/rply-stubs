from typing import Callable, Literal, Never

def rightmost_terminal(
    symbols: list[str], terminals: dict[str, list[int]]
) -> str | None: ...

type PrecedenceAssociativity = Literal["left"] | Literal["right"] | Literal["nonassoc"]
type PrecedenceTuple = tuple[PrecedenceAssociativity, int]

type ProductionFunction = Callable

class Grammar(object):
    productions: list["None | Production"]
    prod_names: dict[str, list["Production"]]
    terminals: dict[str, list[int]]

    nonterminals: dict[str, list[int]]
    first: dict[str, list[str]]
    follow: dict[str | None, list[str]]
    precedence: dict[str | None, PrecedenceTuple]
    start: str | None

    def __init__(self, terminals: list[str]): ...
    def add_production(
        self,
        prod_name: str,
        syms: list[str],
        func: ProductionFunction,
        precedence: str | None,
    ) -> None | Never: ...
    def set_precedence(
        self, term: str, assoc: PrecedenceAssociativity, level: int
    ) -> None | Never: ...
    def set_start(self) -> None: ...
    def unused_terminals(self) -> list[str]: ...
    def unused_productions(self) -> list[str]: ...
    def build_lritems(self) -> None: ...
    def _first(self, beta: str) -> list[str]: ...
    def compute_first(self) -> None: ...
    def compute_follow(self) -> None: ...

class Production(object):
    number: int
    name: str
    prod: list[str]
    func: ProductionFunction | None
    prec: PrecedenceTuple
    unique_syms: list[str]

    lr_items: list["LRItem | None"]
    lr_next: "LRItem | None"
    lr0_added: int
    reduced: int

    def __init__(
        self,
        num: int,
        name: str,
        prod: list[str],
        precedence: PrecedenceTuple,
        func: ProductionFunction | None,
    ): ...
    def __repr__(self) -> str: ...
    def getlength(self) -> int: ...

class LRItem(object):
    name: str
    prod: list[str]
    number: int
    lr_index: int
    lookaheads: dict[Unknown, list[Unknown]]
    unique_syms: list[str]
    lr_before: str | None
    lr_after: list[Production]

    def __init__(
        self, p: Production, n: int, before: str | None, after: list[Production]
    ):
        self.name = p.name
        self.prod = p.prod[:]
        self.prod.insert(n, ".")
        self.number = p.number
        self.lr_index = n
        self.lookaheads = {}
        self.unique_syms = p.unique_syms
        self.lr_before = before
        self.lr_after = after

    def __repr__(self) -> str: ...
    def getlength(self) -> int: ...
