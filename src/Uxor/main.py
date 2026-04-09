from argparse import ArgumentParser
from collections.abc import Generator
import copy
from enum import Enum
import enum
import inspect
import re
from re import Pattern
from typing import Any


AddReplacements = dict[str | Pattern | frozenset[str], str]
FindReplace = list[tuple[str, str]]


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


class LineBreak(Enum):
    """
    AFTER_SENTENCE: The breaking ideographic spaces already inserted
      between sentences will be the only breaking characters in the
      output.
    WHEN_UNAMBIGUOUS: Breaking zero-width spaces will be inserted after
      matches of the object's UNAMBIGUOUS_LINEBREAK_REGEX (defaults to 
      `e|en|la|li`).
    AFTER_ANY_GLYPH: Breaking zero-width spaces will be inserted after
      every glyph.
    """
    AFTER_SENTENCE = enum.auto()
    WHEN_UNAMBIGUOUS = enum.auto()
    AFTER_ANY_GLYPH = enum.auto()


class StandardUxor:
    WORD_SEPARATOR_IN_INPUT = " "
    REPLACEMENTS = {  # @TODO: All UCSUR codepoints.
        "te": "「",
        "to": "」",
        "a": "\U000F1900",
        "akesi": "\U000F1901",
        "ala": "\U000F1902",
        "alasa": "\U000F1903",
        "ale": "\U000F1904",
        "ali": "\U000F1904",
        "anpa": "\U000F1905",
        "ante": "\U000F1906",
        "anu": "\U000F1907",
        "awen": "\U000F1908",
        "e": "\U000F1909",
        "en": "\U000F190A",
        "esun": "\U000F190B",
        "ijo": "\U000F190C",
        "ike": "\U000F190D",
        "ilo": "\U000F190E",
        "insa": "\U000F190F",
        "jaki": "\U000F1910",
        "jan": "\U000F1911",
        "jelo": "\U000F1912",
        "jo": "\U000F1913",
        "kala": "\U000F1914",
        "kalama": "\U000F1915",
        "kama": "\U000F1916",
        "kasi": "\U000F1917",
        "ken": "\U000F1918",
        "kepeken": "\U000F1919",
        "kili": "\U000F191A",
        "kiwen": "\U000F191B",
        "ko": "\U000F191C",
        "kon": "\U000F191D",
        "kule": "\U000F191E",
        "kulupu": "\U000F191F",
        "kute": "\U000F1920",
        "la": "\U000F1921",
        "lape": "\U000F1922",
        "laso": "\U000F1923",
        "lawa": "\U000F1924",
        "len": "\U000F1925",
        "lete": "\U000F1926",
        "li": "\U000F1927",
        "lili": "\U000F1928",
        "linja": "\U000F1929",
        "lipu": "\U000F192A",
        "loje": "\U000F192B",
        "lon": "\U000F192C",
        "luka": "\U000F192D",
        "lukin": "\U000F192E",
        "lupa": "\U000F192F",
        "ma": "\U000F1930",
        "mama": "\U000F1931",
        "mani": "\U000F1932",
        "meli": "\U000F1933",
        "mi": "\U000F1934",
        "mije": "\U000F1935",
        "moku": "\U000F1936",
        "moli": "\U000F1937",
        "monsi": "\U000F1938",
        "mu": "\U000F1939",
        "mun": "\U000F193A",
        "musi": "\U000F193B",
        "mute": "\U000F193C",
        "nanpa": "\U000F193D",
        "nasa": "\U000F193E",
        "nasin": "\U000F193F",
        "nena": "\U000F1940",
        "ni": "\U000F1941",
        "nimi": "\U000F1942",
        "noka": "\U000F1943",
        "o": "\U000F1944",
        "olin": "\U000F1945",
        "ona": "\U000F1946",
        "open": "\U000F1947",
        "pakala": "\U000F1948",
        "pali": "\U000F1949",
        "palisa": "\U000F194A",
        "pan": "\U000F194B",
        "pana": "\U000F194C",
        "pi": "\U000F194D",
        "pilin": "\U000F194E",
        "pimeja": "\U000F194F",
        "pini": "\U000F1950",
        "pipi": "\U000F1951",
        "poka": "\U000F1952",
        "poki": "\U000F1953",
        "pona": "\U000F1954",
        "sama": "\U000F1956",
        "seli": "\U000F1957",
        "selo": "\U000F1958",
        "seme": "\U000F1959",
        "sewi": "\U000F195A",
        "sijelo": "\U000F195B",
        "sike": "\U000F195C",
        "sin": "\U000F195D",
        "sina": "\U000F195E",
        "sinpin": "\U000F195F",
        "sitelen": "\U000F1960",
        "sona": "\U000F1961",
        "soweli": "\U000F1962",
        "suli": "\U000F1963",
        "suno": "\U000F1964",
        "supa": "\U000F1965",
        "suwi": "\U000F1966",
        "tan": "\U000F1967",
        "taso": "\U000F1968",
        "tawa": "\U000F1969",
        "telo": "\U000F196A",
        "tenpo": "\U000F196B",
        "toki": "\U000F196C",
        "tomo": "\U000F196D",
        "tu": "\U000F196E",
        "unpa": "\U000F196F",
        "uta": "\U000F1970",
        "utala": "\U000F1971",
        "walo": "\U000F1972",
        "wan": "\U000F1973",
        "waso": "\U000F1974",
        "wawa": "\U000F1975",
        "weka": "\U000F1976",
        "wile": "\U000F1977",
        "namako": "\U000F1978",
        "kin": "\U000F1979",
        "kipisi": "\U000F197B",
        "leko": "\U000F197C",
        "monsuta": "\U000F197D",
        "tonsi": "\U000F197E",
        "jasima": "\U000F197F",
        "soko": "\U000F1981",
        "meso": "\U000F1982",
        "lanpan": "\U000F1985",
        "n": "\U000F1986",
        "misikeke": "\U000F1987",
        "majuna": "\U000F19A2",
        "zz": "\u200D", #  zero-width joiner 
        "[": "\U000F1990", #  cartouche start 
        "]": "\U000F1991", #  cartouche end 
        "-": "\U000F1995", #  stacking joiner 
        "+": "\U000F1996", #  scaling joiner 
        "(": "\U000F1997", #  long glyph start 
        ")": "\U000F1998", #  long glyph end 
        ".": "\U000F199C", #  middot 
        ":": "\U000F199D", #  colon
        "\n": "\n"
    }
    # SENTENCE_SEPARATOR_IN_OUTPUT = "\u3000"  # "　"
    # STACK_JOINER = "-"
    # NEST_JOINER = "+"
    # SPECIAL_JOINER = "&"
    # CARTOUCHE_OPENER = "["
    # CARTOUCHE_CONTINUER = "="
    # CARTOUCHE_CLOSER = "]"
    # PI_OPENER = "("
    # PI_CONTINUER = "_"
    # PI_CLOSER = ")"

    SPECIAL_CHAR_REGEX = re.compile(r"([-+&[=\](_)])")
    UNAMBIGUOUS_LINEBREAK_REGEX = re.compile(
        r"[\U000F1909\U000F190A\U000F1921\U000F1927]")  # 󱤉󱤊󱤡󱤧
    VARIANT_REGEX = re.compile(r"(.+)(\d+|(?<=ni)[\^><v])?")

    def __init__(self,
                 allow_unspaced: bool = False,
                 report_invalid: bool = False,
                 line_break: LineBreak = LineBreak.AFTER_SENTENCE):
        self.allow_unspaced = allow_unspaced
        self.report_invalid = report_invalid
        self.line_break = line_break
        self.parse_sequence = (self.decode_unspaced if self.allow_unspaced
                               else self.lookup_word)

    def __call__(self, text: str) -> str:
        normalized = self.normalize(text)
        separated = normalized.split(self.WORD_SEPARATOR_IN_INPUT)
        try:
            decoded = [self.decode(seq) for seq in separated]
        except InvalidSequence as e:
            if self.report_invalid:
                return f"[SITELEN IKE: {e.args[0]}]"
            return text
        compiled = self.compile(decoded)
        return compiled

    @classmethod
    def cli(cls) -> None:
        signature = inspect.signature(cls.__init__)
        # @TODO: Get info from docstring, pass to `help=` in 
        # `add_argument`.
        # documentation = inspect.getdoc(cls.__init__)
        arg_parser = ArgumentParser()
        arg_parser.add_argument('text', nargs='*')
        for parameter in signature.parameters.values():
            if parameter.name != 'self':
                arg_parser.add_argument(f"--{parameter.name}",
                                        default=parameter.default)
                parameter.annotation
        args = vars(arg_parser.parse_args())
        text = args['text']
        del args['text']
        init_kwargs = {k: signature.parameters[k].annotation(v)
                       for k, v in args.items()}
        instance = cls(**init_kwargs)
        if text:
            print(instance(" ".join(text)))
        else:
            print("o pana e sitelen Lasina.")
            while True:
                print(instance(input("> ")))

    def normalize(self, text: str) -> str:
        """Normalizes any quirks in the input.
        
        In the standard implementation of Uxor, the only thing this does
        is convert multiple consecutive spaces (U+20) to a single space.
        """
        normalized = re.sub(r" +", self.WORD_SEPARATOR_IN_INPUT, text)
        return normalized

    def decode(self, sequence: str) -> str:
        # We reuse WORD_SEPARATOR_IN_INPUT because it's guaranteed not
        # to appear elsewhere in the string.
        spaced = self.SPECIAL_CHAR_REGEX.sub(
            fr"{self.WORD_SEPARATOR_IN_INPUT}\1{self.WORD_SEPARATOR_IN_INPUT}",
            sequence
        )
        words = spaced.split(self.WORD_SEPARATOR_IN_INPUT)
        try:
            decoded = [i for w in words for i in self.parse_sequence(w)]
        except UnresolvedSequence as e:
            raise InvalidSequence(e.args[0]) from e
        compiled = self.compile(decoded)
        return compiled
    
    def decode_unspaced(self, sequence: str) -> list[str]:
        decoded = []
        try:
            decoded = self.lookup_word(sequence)
        except UnresolvedSequence as e:
            if len(sequence) == 1:
                raise InvalidSequence(sequence) from e
            for idx in range(1, len(sequence))[::-1]:
                try:
                    decoded += self.lookup_word(sequence[:idx])
                except UnresolvedSequence:
                    continue
                else:
                    # If we've reached 0, it's back to the original
                    # sequence.
                    if idx:
                        decoded += self.decode_unspaced(sequence[idx:])
                        break
            else:
                raise InvalidSequence(sequence) from e
        return decoded

    def lookup_word(self, word: str) -> list[str]:
        try:
            base_word, variant_indicator = self.VARIANT_REGEX.match(word).groups()
        except AttributeError as e:
            print(f"Invalid sequence {word}")
            raise InvalidSequence(word) from e
        try:
            base_glyph = self.REPLACEMENTS[base_word]
        except KeyError as e:
            raise UnresolvedSequence(word) from e
        return [f"{base_glyph}{variant_indicator or ''}"]

    def compile(self, sequences: list[str]) -> str:
        match self.line_break:
            case LineBreak.AFTER_SENTENCE:
                spaced = sequences
            case LineBreak.WHEN_UNAMBIGUOUS:
                spaced = [
                    f"{s}\u200B" if self.UNAMBIGUOUS_LINEBREAK_REGEX.match(s)
                    else s for s in sequences]
            case LineBreak.AFTER_ANY_GLYPH:
                spaced = [f"{s}\u200B" for s in sequences]
        compiled = "".join(spaced)
        return compiled
