# Don't change this line!
import re

from uxor.main import LineBreak, ReportInvalid, Uxor


class PankantanUxor(Uxor):
    """This is probably not an Uxor you want to use.

    It is highly customized to a specific project where the ASCII input
    uses a mix of styles and where there are very particular needs for
    the output.  However, it is included in the prefabs module to
    demonstrate what a highly customized Uxor looks like.    
    """
    INP_WORD_SEP_RE = re.compile(r"[^\S\n\u3000]+")  # U3000 = Ideographic space
    OUT_VAR_JOINER = ""
    LINE_BREAK_RES = Uxor.LINE_BREAK_RES | {
        LineBreak.WHEN_UNAMBIGUOUS: re.compile(r"([\U000F1909\U000F190A\U000F1927\U000F199C]|(?<!\s)\U000F1921)(?!\u200B|[^\U000F1990]*\U000F1991)")
    }
    BASE_WORD_REPLS = Uxor.BASE_WORD_REPLS
    # The ".." and "::" keys need to come first in the dict, so these
    # have to be removed initially.
    del BASE_WORD_REPLS["."], BASE_WORD_REPLS[":"]
    BASE_WORD_REPLS |= {
        "nn": " ",
        "mm": "  ",
        "\u3000": " ",  # Ideographic space
        "\n": "  ",
        "xx": "\u2588",  # █
        "te": "\U000F19B4",  # Custom codepoint for LO compatibility reasons
        "to": "\U000F19B5",  # Ditto
        # ".." within cartouches have been handled in `normalize`
        "..": "\U000F199C",  # Treat double-dot like single
        "::": "\U000F199D",  # Ditto with colon
        ".": "\U000F199C",  # Now we can add these back
        ":": "\U000F199D",
        "\uFE00": "1",  # Variation selectors
        "\uFE01": "2",
        "\uFE02": "3",
        "\uFE03": "4",
        "\u2193": "1",  # Directional arrows
        "\u2192": "2",
        "\u2190": "3",
        "\u2191": "4",
        "v": "1",
        ">": "2",
        "<": "3",
        "^": "4"
    }

    def __init__(
            self,
            allow_unspaced: bool = True,
            ignore_variants: bool = False,
            report_invalid: ReportInvalid = ReportInvalid.UNLESS_VALID_REPLACEMENT,
            line_break: LineBreak = LineBreak.WHEN_UNAMBIGUOUS):
        super().__init__(allow_unspaced, ignore_variants, report_invalid, line_break)

    def normalize(self, text: str):
        # Remove zero-width spaces, zero-width joiners, and cartuche
        # extenders in input
        de_invisibled = re.sub(r"[\u200B\u200C\U000F1992]", "", text)
        cartouche_dots_preconverted = re.sub(
            r"([^\[\U000F1990][\]\U000F1991]*)\.{2}",
            "\\1\U000F199C\U000F199C",
            de_invisibled)
        return cartouche_dots_preconverted

    def compile(self, sequences):
        spaced = super().compile(sequences)
        condensed = re.sub(r" {2,}", "  ", spaced)
        arrow_rotated = re.sub("\U000F19414", "\U000F19413", condensed)
        cartouche_linebroken = re.sub(
            r"(\U000F1990[^\U000F1991]*[^\U000F1991\U000F1995\U000F1996])([\U000F1900-\U000F1987\U000F19A2](?:(?:[\U000F1995\U000F1996][\U000F1900-\U000F1987\U000F19A2]){0,2}|\U000F199C+|\U000F199D))([\u200B\U000F1991])",
            "\\1\u200B\\2\U000F1992\\3",
            arrow_rotated)
        return cartouche_linebroken


if __name__ == "__main__":
    PankantanUxor().cli()
