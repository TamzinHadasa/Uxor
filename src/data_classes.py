import copy
from re import Pattern
from typing import Any


class UxorError(Exception): pass

class ConfigError(UxorError): pass

class UnresolvedSequence(UxorError, ValueError): pass

class InvalidSequence(UxorError, ValueError): pass


class MultiKeyDict(dict[Any, Any]):
    """Dict that treats members of frozenset keys as keys themselves.
    
    For a dict like `foo = MultiKeyDict({frozenset({1, 2, 3, 4, 5}): True})`:
    * `foo[1]` -> `True`
    * `del foo[1]` -> `MultiKeyDict({frozenset({2, 3, 4, 5}): True})`
    * `foo[2] = False` -> `MultiKeyDict({frozenset({3, 4, 5}): True, 2: False})`
    * `foo | {3: None}` -> `MultiKeyDict({frozenset({4, 5}): True, 2: False, 3: None})`

    Raises:
      ConfigError if the same query key appears in two frozenset keys, or as a
      key of its own and in a frozenset key.
    """
    def _find_query_key_in_keys(self, query_key):
        matches = [k for k in self.keys()
                   if (k == query_key) or (isinstance(k, frozenset)
                                           and query_key in k)]
        if not matches:
            raise KeyError
        if len(matches) > 1:
            raise ConfigError(f"{__class__} has value {query_key} in multiple entries: {matches}")
        return matches[0]

    def __getitem__(self, query_key: Any) -> Any:
        get_key = self._find_query_key_in_keys(query_key)
        return super().__getitem__(get_key)

    def __setitem__(self, query_key: Any, value: Any) -> None:
        if isinstance(query_key, frozenset):
            for subkey in query_key:
                super().__setitem__(subkey, value)
            return
        try:
            set_key = self._find_query_key_in_keys(query_key)
        except KeyError:
            pass
        else:
            if set_key != query_key:
                new_set = set(set_key)
                new_set.remove(query_key)
                super().__setitem__(frozenset(new_set), self[set_key])
                del self[set_key]
        super().__setitem__(query_key, value)

    def __delitem__(self, query_key: Any) -> None:
        if (del_key := self._find_query_key_in_keys(query_key)) != query_key:
            new_set = set(del_key)
            new_set.remove(query_key)
            self[frozenset(new_set)] = self[del_key]
        super().__delitem__(del_key)

    def __or__(self, other: dict[Any, Any]) -> 'MultiKeyDict':
        new_dict = copy.deepcopy(self)
        for k, v in other.items():
            new_dict[k] = v
        return new_dict

    def __ior__(self, other) -> 'MultiKeyDict': # type: ignore[misc]
        for k, v in other.items():
            self[k] = v
        return self


class ReplacementDict(MultiKeyDict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.patterns: dict[Pattern, Any] = {}
        self._update_patterns()

    def __getitem__(self, query_key):
        if isinstance(query_key, str):
            for pattern, repl in self.patterns.items():
                if pattern.match(query_key):
                    return repl
        try:
            return super().__getitem__(query_key)
        except KeyError:
            if query_key in self.values():
                return query_key
            raise

    def __setitem__(self, query_key, value):
        super().__setitem__(query_key, value)
        self._update_patterns()

    def _update_patterns(self):
        self.patterns = {k: v for k, v in self.items()
                         if isinstance(k, Pattern)}
