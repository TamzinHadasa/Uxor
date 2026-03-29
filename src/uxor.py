from collections.abc import Callable
import re

from data_classes import MultiKeyDict


AddReplacements = dict[str | tuple[str, ...], str]


class Uxor:
    default_replacements = MultiKeyDict({  # @TODO: All UCSUR codepoints.
        ("te", "“"): "「",
        ("to", "”"): "」",
        "a": "\U000F1900",
        "akesi": "\U000F1901",
        "ala": "\U000F1902",
        "alasa": "\U000F1903",
        ("ale", "ali"): "\U000F1904",
        "anpa": "\U000F1905",
        "ante": "\U000F1906",
        "anu": "\U000F1907",
        "awen": "\U000F1908",
        "e": "\U000F1909",
        "en": "\U000F190a",
        "esun": "\U000F190b",
        "ijo": "\U000F190c",
        "ike": "\U000F190d",
        "ilo": "\U000F190e",
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
        "kili": "\U000F191a",
        "kiwen": "\U000F191b",
        "ko": "\U000F191c",
        "kon": "\U000F191d",
        "kule": "\U000F191e",
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
        "lipu": "\U000F192a",
        "loje": "\U000F192b",
        "lon": "\U000F192c",
        "luka": "\U000F192d",
        "lukin": "\U000F192e",
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
        "mun": "\U000F193a",
        "musi": "\U000F193b",
        "mute": "\U000F193c",
        "nanpa": "\U000F193d",
        "nasa": "\U000F193e",
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
        "palisa": "\U000F194a",
        "pan": "\U000F194b",
        "pana": "\U000F194c",
        "pi": "\U000F194d",
        "pilin": "\U000F194e",
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
        "sewi": "\U000F195a",
        "sijelo": "\U000F195b",
        "sike": "\U000F195c",
        "sin": "\U000F195d",
        "sina": "\U000F195e",
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
        "telo": "\U000F196a",
        "tenpo": "\U000F196b",
        "toki": "\U000F196c",
        "tomo": "\U000F196d",
        "tu": "\U000F196e",
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
        "kipisi": "\U000F197b",
        "leko": "\U000F197c",
        "monsuta": "\U000F197d",
        "tonsi": "\U000F197e",
        "jasima": "\U000F197F",
        "soko": "\U000F1981",
        "meso": "\U000F1982",
        "lanpan": "\U000F1985",
        "n": "\U000F1986",
        "misikeke": "\U000F1987",
        "majuna": "\U000F19a2",
        "zz": "\u200D", #  zero-width joiner 
        "[": "\U000F1990", #  cartouche start 
        "]": "\U000F1991", #  cartouche end 
        "-": "\U000F1995", #  stacking joiner 
        "+": "\U000F1996", #  scaling joiner 
        "(": "\U000F1997", #  long glyph start 
        ")": "\U000F1998", #  long glyph end 
        ".": "\U000F199C", #  middot 
        ":": "\U000F199D", #  colon
        ("\uFE00", "\u2190", "<"): "1",
        ("\uFE01", "\u2191", "^"): "2",
        ("\uFE02", "\u2192", ">"): "3",
        ("\uFE03", "\u2193", "v"): "4",
        ("\uFE04", "\u2196", "<^", "^<"): "5",
        ("\uFE05", "\u2197", ">^", "^>"): "6",
        ("\uFE06", "\u2198", "v>", ">v"): "7",
        ("\uFE07", "\u2199", "<v", "v<"): "8"
    })
    def __init__(self,
                 *,
                 add_replacements: AddReplacements | None = None,
                 remove_keys: list[str] | None = None,
                 before_find: str = "",
                 before_replace: str = "",
                 separation_find: str = r"\s+",
                 separation_replace: str = " ",
                 after_find: str = "",
                 after_replace: str  = ""
                 ):
        self.__name__ = self.__class__.__name__  # Needed for LibreOffice.
        add_replacements = (add_replacements
                            if add_replacements is not None else {})
        remove_keys = remove_keys if remove_keys is not None else []
        self.replacements = self.default_replacements | add_replacements
        for k in self.replacements:
            if k in remove_keys:
                del self.replacements[k]
        self.prepare: Callable[[str], str] = (
            lambda x: re.sub(before_find, before_replace, x)
            if before_find else x
        )
        self.separator = separation_replace
        self.separate: Callable[[str], str] = (
            lambda x: re.sub(separation_find, separation_replace, x)
            if separation_find else x
        )
        self.tidy: Callable[[str], str] = (
            lambda x: re.sub(after_find, after_replace, x)
            if after_find else x
        )
    
    # Having the object be callable makes LibreOffice happy.
    def __call__(self, input_: str) -> str:
        sanitized = self.sanitize(input_)
        separated = sanitized.split(self.separator)
        sequences = [self.decode_seq(seq) for seq in separated]
        spaced = self.space(sequences)
        return spaced

    def sanitize(self, input_: str) -> str:
        stripped = input_.strip()
        prepared = self.prepare(stripped)
        separated = self.separate(prepared)
        return separated

    def decode_seq(self, seq: str) -> str:
        words = ""
        try:
            words = self.get_word(seq)
        except ValueError:
            if len(seq) == 1:
                raise
            else:
                for idx in range(len(seq))[::-1]:
                    try:
                        words += self.get_word(seq[:idx])
                    except ValueError:
                        continue
                    else:
                        words += self.decode_seq(seq[idx:])
                        break
                else:
                    raise
        return words
    
    def get_word(self, seq: str) -> str:
        try:
            return self.replacements[seq]
        except KeyError as e:
            if len(seq) == 1:
                if seq in self.replacements.values():
                    return seq
            raise ValueError(seq) from e
    
    def space(self, sequences: list[str]) -> str:
        joined = "".join(sequences)
        tidied = self.tidy(joined)
        return tidied
