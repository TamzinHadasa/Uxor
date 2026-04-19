from enum import Enum
import re


class UxorError(Exception): pass

class UnresolvedSequence(UxorError, ValueError): pass

class InvalidSequence(UxorError, ValueError): pass


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
    AFTER_SENTENCE = 0
    WHEN_UNAMBIGUOUS = 1
    AFTER_WORD_GROUP = 2


class ReportInvalid(Enum):
    NEVER = 0
    UNLESS_VALID_REPLACEMENT = 1
    ALWAYS = 2


class Uxor:
    INP_WORD_SEP = " "  # Literal space (U+20)
    OUT_SENTENCE_SEP = "\u3000"  # "　"
    OUT_VAR_JOINER = "\u200D"  # Zero-width joiner

    INP_WORD_SEP_RE = re.compile(fr"{INP_WORD_SEP}+")
    SPECIAL_CHAR_RE = re.compile(r"([-+&[=\](_)])")
    DIR_VAR_RE = re.compile(r"[\^><v]")
    DIR_WORDS_RE = re.compile(r"ni")
    VAR_RE = re.compile(
        fr"""(.+?)  # Capture the shortest matching sequence of 1+ characters.
             (  # Either:
              \d+  # the longest matching sequence of 1+ digits
             |  # --or--
              (?<={DIR_WORDS_RE.pattern})  # where following this← pattern,
              {DIR_VAR_RE.pattern}  # this← pattern,
             )?  # --or-- nothing at all.
             $  # End of string.
        """,
        flags=re.VERBOSE)

    _CLI_PROMPT = "o pana e sitelen Lasina."
    _CLI_INPUT_LINE = "> "
    _INVALID_SEQ_MESSAGE = "[SITELEN IKE: {}]"

    LINE_BREAK_RES = {
        # LineBreak.AFTER_SENTENCE: re.compile(fr".(?={OUTPUT_SENTENCE_SEPARATOR}|$)"),
        LineBreak.WHEN_UNAMBIGUOUS: re.compile(
            r"([\U000F1909\U000F190A\U000F1921\U000F1927])"),  # 󱤉󱤊󱤡󱤧
        LineBreak.AFTER_WORD_GROUP: re.compile(
            r"""(  # Either:
                 [\U000F1900-\U000F198C\U000F19A0-\U000F19BA]  # A word glyph,
                 (?:  # followed by either
                  [\u200D\U000F1995\U000F1996]  # a ZWJ, stacking joiner, or scaling joiner,
                  [\U000F1900-\U000F198C\U000F19A0-\U000F19BA]  # and another word glyph
                 |  # --or--
                  \u200D  # a ZWJ
                  [0-9]+  # and one or more Arabic numerals
                 )*  # zero to infinity times;
                |  # --or--
                 [\U000F1991\U000F1998]  # a cartouche end or long-glyph end.
                )
            """,
            flags=re.VERBOSE)
    }
    # Values taken from <https://github.com/lipu-linku/sona/tree/main/glyphs/metadata>
    # as compiled at <https://sitelenpona.net/ascii.html#standard-glyph-numbering>.
    # If you change this attribute in a subclass, you're doing ni 
    # replacement surgery.
    DIR_VAR_REPLS = {
        "v": "01",
        ">": "02",
        "^": "03",
        "<": "04",
        "v>": "05",
        ">v": "05",
        "^>": "06",
        ">^": "06",
        "^<": "07",
        "<^": "07",
        "v<": "08",
        "<v": "08"
    }
    BASE_WORD_REPLS = {  # @TODO: All UCSUR codepoints.
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

    # STACK_JOINER = "-"
    # NEST_JOINER = "+"
    # SPECIAL_JOINER = "&"
    # CARTOUCHE_OPENER = "["
    # CARTOUCHE_CONTINUER = "="
    # CARTOUCHE_CLOSER = "]"
    # PI_OPENER = "("
    # PI_CONTINUER = "_"
    # PI_CLOSER = ")"

    def __init__(self,
                 allow_unspaced: bool = False,
                 ignore_variants: bool = False,
                 report_invalid: ReportInvalid = ReportInvalid.NEVER,
                 line_break: LineBreak = LineBreak.AFTER_SENTENCE):
        self.allow_unspaced = allow_unspaced
        self.ignore_variants = ignore_variants
        self.report_invalid = report_invalid
        self.line_break = line_break
        self.line_break_regex = self.LINE_BREAK_RES.get(line_break)
        self.parse_sequence = (self.decode_unspaced if self.allow_unspaced
                               else self.get_replacement)

    def __call__(self, text: str) -> str:
        normalized = self.normalize(text)
        separated = self.INP_WORD_SEP_RE.split(normalized)
        decoded = []
        for _ in range(len(separated)):
            seq = separated.pop(0)
            try:
                decoded_seq = self.decode(seq)
            except InvalidSequence:
                decoded_seq = self._handle_invalid(seq,
                                                   final=not any(separated))
            decoded.append(decoded_seq)
        compiled = self.compile(decoded)
        return compiled

    def _handle_invalid(self, sequence: str, *, final: bool) -> str:
        return (
            (self._INVALID_SEQ_MESSAGE.format(sequence)
             if self._should_report(sequence) else sequence)
            + (self.INP_WORD_SEP if not final else "")
        )

    def _should_report(self, sequence: str) -> bool:
        if self.report_invalid == ReportInvalid.UNLESS_VALID_REPLACEMENT:
            return any ([i not in self.BASE_WORD_REPLS.values()
                        for i in sequence])
        return bool(self.report_invalid.value)

    def normalize(self, text: str) -> str:
        """Normalizes any quirks in the input.
        
        In the standard implementation of Uxor, this does not do
        anything.
        """
        return text

    def decode(self, sequence: str) -> str:
        # We reuse INPUT_WORD_SEPARATOR because it's guaranteed not
        # to appear elsewhere in the string.
        spaced = self.SPECIAL_CHAR_RE.sub(
            fr"{self.INP_WORD_SEP}\1{self.INP_WORD_SEP}",
            sequence
        )
        subsequences = self.INP_WORD_SEP_RE.split(spaced)
        try:
            decoded = [i for ss in subsequences
                       for i in self.parse_sequence(ss)]
        except UnresolvedSequence as e:
            raise InvalidSequence(e.args[0]) from e
        joined = "".join(decoded)
        return joined
    
    def decode_unspaced(self, sequence: str) -> list[str]:
        decoded = []
        try:
            decoded = self.get_replacement(sequence)
        except UnresolvedSequence as e:
            if len(sequence) == 1:
                raise InvalidSequence(sequence) from e
            for idx in range(1, len(sequence))[::-1]:
                try:
                    decoded += self.get_replacement(sequence[:idx])
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

    def get_replacement(self, sequence: str) -> list[str]:
        try:
            base_word, inp_variant_code = (self.VAR_RE.match(sequence)
                                           .groups())  # type: ignore[union-attr]
        except AttributeError as e:
            raise InvalidSequence(sequence) from e
        else:
            base_word: str
            inp_variant_code: str
        try:
            base_glyph = self.BASE_WORD_REPLS[base_word]
        except KeyError as e:
            raise UnresolvedSequence(sequence) from e
        if not self.ignore_variants and inp_variant_code:
            out_variant_code = self.DIR_VAR_REPLS.get(
                inp_variant_code, inp_variant_code)
            variant_suffix = self.OUT_VAR_JOINER + out_variant_code
        else:
            variant_suffix = ""
        return [base_glyph + variant_suffix]

    def compile(self, sequences: list[str]) -> str:
        joined = "".join(sequences)
        spaced = (self.line_break_regex.sub("\\1\u200B", joined)
                  if self.line_break_regex else joined)
        return spaced

    def cli(self, text: str = "") -> None:
        if text:
            print(self(text))
        else:
            print(self._CLI_PROMPT)
            while True:
                print(self(input(self._CLI_INPUT_LINE)))


if __name__ == "__main__":
    Uxor().cli()
