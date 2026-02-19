from uxor import NumberVariantStyle, Uxor  # Don't change this line!

default = Uxor()  # Don't change this line

# You can now define Uxor objects with different configs below.  For instance,
# here is something from a working project of mine.
pankantan = Uxor(
    # Replaces these special sequences with spaces.
    # Note that if you want to merely amend the default replacements 
    # (overwriting existing ones in case of conflict), you should set:
    #     replacements=Uxor.default_replacements | { ...
    # If you want to completely overwrite the default replacements, you should
    # set:
    #     replacements={ ...
    replacements=Uxor.default_replacements | {
        "nn": " ",
        "mm": "  "
    },
    # Replaces all zero-width non-joiners with the default before_replace value,
    # which is nothing.  (I.e, it removes them.)  If we wanted to replace them
    # with something else, we'd also add `before_replace`.
    before_find=r"[\u200C]",
    # Replaces any instance of U+F1909 (e) or U+F1927 (li), plus any instance of
    # U+F1921 (la) that doesn't follow a space, with themself plus U+200B (zero-
    # width space) (i.e., it adds U+200B after the character), unless there are
    # no U+F1990 (cartouche start) before the next U+F1991 (cartouche end) 
    # (i.e., we are mid-cartouche).
    after_find=r"([\U000F1909\U000F1927]|(?<!\s)\U000F1921)(?![^\U000F1990]*\U000F1991)",
    after_replace="\\1\u200B",
    # These next two are the default values, so not actually necessary, but 
    # included here for illustration.
    number_variant_style=NumberVariantStyle.NUMERAL,  # `ni3`, for instance.
    variant_joiner=""  # No zero-width joiner or anything like that in `ni3`.
)

# Example constructor for a new Uxor object.  Remove any lines that you don't
# change.
my_uxor = Uxor (
    # Remove `Uxor.default_replacements | ` if you want to overwrite the entire
    # replacement table.
    replacements=Uxor.default_replacements | {
        # Put values here like: "word": "replacement",
    },
    # NumberVariantStyle.NUMERAL, NumberVariantStyle.VARIATION_SELECTOR, 
    # NumberVariantStyle.UNICODE_ARROW, or NumberVariantStyle.ASCII_ARROW
    number_variant_style=NumberVariantStyle.NUMERAL,
    # Some string to go between a glyph and the variant symbol after it
    variant_joiner="",
    # These next bits involve regular expressions (regexes).  See <https://www.regular-expressions.info/>
    # for information and <https://regex101.com/> for troubleshooting.
    #
    # Before doing anything else to the input, find things matching this 
    # regex...
    before_find="",
    # ... and replace them with this string:
    before_replace="",
    # Then find things matching this regex...
    separation_find=r"\s+",
    # ... and replace them with this, which will be used to break the input into
    # words:
    separation_replace=" ",
    # After doing all replacements, find things matching this regex...
    after_find="",
    # ... and replace them with this:
    after_replace=""
)