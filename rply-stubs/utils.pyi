import sys
from typing import Generator, ItemsView, ValuesView

if sys.version_info >= (3, 3):
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


class IdentityDict[K: object, V: object](MutableMapping):
    _contents: dict[int, tuple[K, V, int]]
    _keepalive: list[K]

    def __init__(self):
        ...

    def __getitem__(self, key: K) -> V:
        ...

    def __setitem__(self, key: K, value: V):
        ...

    def __delitem__(self, key: K):
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Generator[K]:
        ...


class Counter(object):
    value: int

    def __init__(self):
        ...

    def incr(self):
        ...


if sys.version_info >= (3,):
    def itervalues[K, V](d: dict[K, V]) -> ValuesView[V]:
        ...

    def iteritems[K, V](d: dict[K, V]) -> ItemsView[K, V]:
        ...
else:
    def itervalues(d):
        return d.itervalues()

    def iteritems(d):
        return d.iteritems()