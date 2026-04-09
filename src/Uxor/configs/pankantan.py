# Don't change this line!
import re

from Uxor.main import Uxor

uxor = Uxor(
    before_find_replace=[
        # Delete unwanted non-printing characters
        (r"[\u200B\u200C\U000F1992]", ""),
        (r"([^\[\U000F1990][\]\U000F1991]*)\.{2}", "\\1\U000F199C\U000F199C")
    ],
    add_replacements={
        re.compile(r"(　\s*){2,}"): "  ",
        "nn": " ",
        "mm": "  ",
        "　": " ",
        "\n": "  ",
        "xx": "\u2588",  # █
        "te": "\U000F19B4",
        "to": "\U000F19B5",
        # ".." within cartouches have been handled in `before_find_replace`
        "..": "\U000F199C",
        "::": "\U000F199D",
        frozenset({"\uFE00", "\u2193", "v"}): "1",
        frozenset({"\uFE01", "\u2192", ">"}): "2",
        frozenset({"\uFE02", "\u2190", "<"}): "3",
        frozenset({"\uFE03", "\u2191", "^"}): "4"
    },
    wordbreak=r"[^\S\n　]+",
    remove_keys=["\uFE04", "\u2196", "<^", "^<",
                 "\uFE06", "\u2198", "v>", ">v",
                 "\uFE05", "\u2197", ">^", "^>",
                 "\uFE07", "\u2199", "<v", "v<",
                 "“", "”"],
    after_find_replace=[
        # Replaces any instance of U+F1909 (e) or U+F1927 (li), plus
        # any instance of U+F1921 (la) that doesn't follow a space, with
        # themself plus U+200B (zero-width space) (i.e., it adds U+200B
        # after the character), unless there are no U+F1990 (cartouche 
        # start) before the next U+F1991 (cartouche end) (i.e., we are 
        # mid-cartouche).
        (r"([\U000F1909\U000F190A\U000F1927\U000F199C]|(?<!\s)\U000F1921)(?!\u200B|[^\U000F1990]*\U000F1991)",
         "\\1\u200B"),
        (r" {2,}", "  "),
        ("\U000F19414", "\U000F19413"),
        (r"(\U000F1990[^\U000F1991]*[^\U000F1991\U000F1995\U000F1996])([\U000F1900-\U000F1987\U000F19A2](?:(?:[\U000F1995\U000F1996][\U000F1900-\U000F1987\U000F19A2]){0,2}|\U000F199C+|\U000F199D))([\u200B\U000F1991])",
         "\\1\u200B\\2\U000F1992\\3")
    ]
)

# Example constructor for a new Uxor object.  Remove any lines that you don't
# change.
# my_uxor = Uxor (
#     # Remove `Uxor.default_replacements | ` if you want to overwrite the entire
#     # replacement table.
#     add_replacements=Uxor.default_replacements | {
#         # Put values here like: "word": "replacement",
#     },
#     # These next bits involve regular expressions (regexes).  See <https://www.regular-expressions.info/>
#     # for information and <https://regex101.com/> for troubleshooting.
#     #
#     # Before doing anything else to the input, find things matching this 
#     # regex...
#     before_find="",
#     # ... and replace them with this string:
#     before_replace="",
#     # Then find things matching this regex...
#     separation_find=r"\s+",
#     # ... and replace them with this, which will be used to break the input into
#     # words:
#     separation_replace=" ",
#     # After doing all replacements, find things matching this regex...
#     after_find="",
#     # ... and replace them with this:
#     after_replace=""
# )