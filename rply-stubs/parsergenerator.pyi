import sys
from typing import Callable, Final, Literal, Never, TypedDict

from .grammar import LRItem, PrecedenceTuple, PrecedenceAssociativity
from rply.grammar import Grammar
from rply.parser import LRParser

from rply.token import Token


LARGE_VALUE = sys.maxsize

type ProductionParts = tuple[str, list[str], Callable, tuple[PrecedenceAssociativity, list[str]] | None]
type Transition = list[tuple[int, LRItem]]
type LookBacks = dict[tuple[int, LRItem], list[tuple[int, list]]]

class ParserGeneratorSerializedTable(TypedDict):
    lr_action: list[dict[str, int]]
    lr_goto: list[dict[str, int]]
    sr_conflicts: list[tuple[int, str, Literal["reduce"] | Literal["nonassoc"] | Literal["shift"]]]
    rr_conflicts: list[tuple[int, str, str]]
    default_reductions: list[int]
    start: str | None
    terminals: list[str]
    precedence: dict[str | None, PrecedenceTuple]
    productions: list[tuple[str, list[str], PrecedenceTuple]]

class ParserGenerator(object):

    VERSION: Final[int]

    tokens: list[Token]
    productions: list[ProductionParts]
    precedence: list[tuple[PrecedenceAssociativity, list[str]]]
    # TODO
    # cache_id: None | ...
    error_handler: None | Callable

    def __init__(self, tokens: list[Token], precedence: list[tuple[PrecedenceAssociativity, list[str]]]=[], cache_id=None):
        ...

    def production(self, rule: str, precedence: tuple[PrecedenceAssociativity, list[str]] | None =None):
        ...

    def error(self, func: Callable) -> Callable:
       ...

    def compute_grammar_hash(self, g: Grammar) -> str:
        ...

    def serialize_table(self, table: "LRTable") -> ParserGeneratorSerializedTable:
        ...

    def data_is_valid(self, g: Grammar, data: ParserGeneratorSerializedTable) -> bool:
        ...

    def build(self) -> LRParser:
        ...

    def _write_cache(self, cache_dir: str, cache_file: str, table: LRTable) -> None | Never:
        ...


# TODO

# def traverse(x, N, stack: list, F, X, R, FP):
#     stack.append(x)
#     d = len(stack)
#     N[x] = d
#     F[x] = FP(x)

#     rel = R(x)
#     for y in rel:
#         if N[y] == 0:
#             traverse(y, N, stack, F, X, R, FP)
#         N[x] = min(N[x], N[y])
#         for a in F.get(y, []):
#             if a not in F[x]:
#                 F[x].append(a)
#     if N[x] == d:
#         N[stack[-1]] = LARGE_VALUE
#         F[stack[-1]] = F[x]
#         element = stack.pop()
#         while element != x:
#             N[stack[-1]] = LARGE_VALUE
#             F[stack[-1]] = F[x]
#             element = stack.pop()


class LRTable(object):
    grammar: Grammar
    lr_action: list[dict[str, int]]
    lr_goto: list[dict[str, int]]
    default_reductions: list[int]
    sr_conflicts: list[tuple[int, str, Literal["reduce"] | Literal["nonassoc"] | Literal["shift"]]]
    rr_conflicts: list[tuple[int, str, str]]

    def __init__(self, grammar: Grammar, lr_action: list[dict[str, int]], lr_goto: list[dict[str, int]], default_reductions: list[int],
                 sr_conflicts: list[tuple[int, str, Literal["reduce"] | Literal["nonassoc"] | Literal["shift"]]], rr_conflicts: list[tuple[int, str, str]]):
        ...

    @classmethod
    def from_cache(cls, grammar: Grammar, data: ParserGeneratorSerializedTable) -> "LRTable":
        ...

    @classmethod
    def from_grammar(cls, grammar: Grammar) -> LRTable | Never:
        ...

    # TODO
    # @classmethod
    # def lr0_items(cls, grammar: Grammar, add_count: Counter, cidhash: IdentityDict, goto_cache: GotoCache) -> list[list[LRItem]]:
    #     C = [cls.lr0_closure([grammar.productions[0].lr_next], add_count)]
    #     for i, I in enumerate(C):
    #         cidhash[I] = i

    #     i = 0
    #     while i < len(C):
    #         I = C[i]
    #         i += 1

    #         asyms = set()
    #         for ii in I:
    #             asyms.update(ii.unique_syms)
    #         for x in asyms:
    #             g = cls.lr0_goto(I, x, add_count, goto_cache)
    #             if not g:
    #                 continue
    #             if g in cidhash:
    #                 continue
    #             cidhash[g] = len(C)
    #             C.append(g)
    #     return C

    # @classmethod
    # def lr0_closure(cls, I: list[LRItem], add_count: Counter) -> list[LRItem]:
    #     add_count.incr()

    #     J = I[:]
    #     added = True
    #     while added:
    #         added = False
    #         for j in J:
    #             for x in j.lr_after:
    #                 if x.lr0_added == add_count.value:
    #                     continue
    #                 J.append(x.lr_next)
    #                 x.lr0_added = add_count.value
    #                 added = True
    #     return J

    # @classmethod
    # def lr0_goto(cls, I: Sequence[Production], x: str, add_count: Counter, goto_cache: GotoCache) -> ...:
    #     s = goto_cache.setdefault(x, IdentityDict())

    #     gs = []
    #     for p in I:
    #         n = p.lr_next
    #         if n and n.lr_before == x:
    #             s1 = s.get(n)
    #             if not s1:
    #                 s1 = {}
    #                 s[n] = s1
    #             gs.append(n)
    #             s = s1
    #     g = s.get("$end")
    #     if not g:
    #         if gs:
    #             g = cls.lr0_closure(gs, add_count)
    #             s["$end"] = g
    #         else:
    #             s["$end"] = gs
    #     return g

    # @classmethod
    # def add_lalr_lookaheads(cls, grammar: Grammar, C: list[list[LRItem]], add_count: Counter, cidhash, goto_cache: GotoCache):
    #     nullable = cls.compute_nullable_nonterminals(grammar)
    #     trans = cls.find_nonterminal_transitions(grammar, C)
    #     readsets = cls.compute_read_sets(grammar, C, trans, nullable, add_count, cidhash, goto_cache)
    #     lookd, included = cls.compute_lookback_includes(grammar, C, trans, nullable, add_count, cidhash, goto_cache)
    #     followsets = cls.compute_follow_sets(trans, readsets, included)
    #     cls.add_lookaheads(lookd, followsets)

    # @classmethod
    # def compute_nullable_nonterminals(cls, grammar: Grammar) -> set[str]:
    #     ...

    # @classmethod
    # def find_nonterminal_transitions(cls, grammar: Grammar, C: list[list[LRItem]]) -> Transition:
    #     trans = []
    #     for idx, state in enumerate(C):
    #         for p in state:
    #             if p.lr_index < p.getlength() - 1:
    #                 t = (idx, p.prod[p.lr_index + 1])
    #                 if t[1] in grammar.nonterminals and t not in trans:
    #                     trans.append(t)
    #     return trans

    # @classmethod
    # def compute_read_sets(cls, grammar: Grammar, C: list[list[LRItem]], ntrans, nullable, add_count: Counter, cidhash, goto_cache: GotoCache):
    #     return digraph(
    #         ntrans,
    #         R=lambda x: cls.reads_relation(C, x, nullable, add_count, cidhash, goto_cache),
    #         FP=lambda x: cls.dr_relation(grammar, C, x, nullable, add_count, goto_cache)
    #     )

    # @classmethod
    # def compute_follow_sets(cls, ntrans, readsets, includesets):
    #     return digraph(
    #         ntrans,
    #         R=lambda x: includesets.get(x, []),
    #         FP=lambda x: readsets[x],
    #     )

    # @classmethod
    # def dr_relation(cls, grammar: Grammar, C: list[list[Production]], trans: tuple[int, str], nullable: set[str], add_count: Counter, goto_cache: GotoCache) -> list[str]:
    #     ...

    # @classmethod
    # def reads_relation(cls, C, trans: Transition, empty, add_count: Counter, cidhash: IdentityDict, goto_cache: GotoCache) -> list[tuple[int, str]]:
    #     rel = []
    #     state, N = trans

    #     g = cls.lr0_goto(C[state], N, add_count, goto_cache)
    #     j = cidhash.get(g, -1)
    #     for p in g:
    #         if p.lr_index < p.getlength() - 1:
    #             a = p.prod[p.lr_index + 1]
    #             if a in empty:
    #                 rel.append((j, a))
    #     return rel

    # @classmethod
    # def compute_lookback_includes(cls, grammar: Grammar, C, trans: Transition, nullable: set[str], add_count: Counter, cidhash: IdentityDict, goto_cache: GotoCache) -> tuple[dict[tuple[int, LRItem], LookBacks], dict[...,...]]:
    #     lookdict = {}
    #     includedict = {}

    #     dtrans = dict.fromkeys(trans, 1)

    #     for state, N in trans:
    #         lookb = []
    #         includes = []
    #         for p in C[state]:
    #             if p.name != N:
    #                 continue

    #             lr_index = p.lr_index
    #             j = state
    #             while lr_index < p.getlength() - 1:
    #                 lr_index += 1
    #                 t = p.prod[lr_index]

    #                 if (j, t) in dtrans:
    #                     li = lr_index + 1
    #                     while li < p.getlength():
    #                         if p.prod[li] in grammar.terminals:
    #                             break
    #                         if p.prod[li] not in nullable:
    #                             break
    #                         li += 1
    #                     else:
    #                         includes.append((j, t))

    #                 g = cls.lr0_goto(C[j], t, add_count, goto_cache)
    #                 j = cidhash.get(g, -1)

    #             for r in C[j]:
    #                 if r.name != p.name:
    #                     continue
    #                 if r.getlength() != p.getlength():
    #                     continue
    #                 i = 0
    #                 while i < r.lr_index:
    #                     if r.prod[i] != p.prod[i + 1]:
    #                         break
    #                     i += 1
    #                 else:
    #                     lookb.append((j, r))

    #         for i in includes:
    #             includedict.setdefault(i, []).append((state, N))
    #         lookdict[state, N] = lookb
    #     return lookdict, includedict

    # @classmethod
    # def add_lookaheads(cls, lookbacks: dict[Transition, LookBacks], followset: dict[Transition, list[tuple[int, list[...]]]]):
    #     for trans, lb in iteritems(lookbacks):
    #         for state, p in lb:
    #             f = followset.get(trans, [])
    #             laheads = p.lookaheads.setdefault(state, [])
    #             for a in f:
    #                 if a not in laheads:
    #                     laheads.append(a)