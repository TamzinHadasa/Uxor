from uxor import NumberVariantStyle, Uxor  # Don't change this line!

default = Uxor()  # Don't change this line

# You can now define Uxor objects with different configs below.  For instance:
pankantan = Uxor(
    replacements=Uxor.default_replacements | {
        "nn": " ",
        "mm": "  "
    },
    ignore_pattern=r"[\u200C]",
    put_space_after_pattern=r"([\U000F1909\U000F1927]|(?<!\s)\U000F1921)(?![^\U000F1990]*\U000F1991)",
    number_variant_style=NumberVariantStyle.NUMERAL
)
# Note that if you want to merely amend the default replacements (overwriting
# existing ones in case of conflict), you should set:
#     replacements=Uxor.default_replacements | { ...
# If you want to completely overwrite the default replacements, you should set:
#     replacements={ ...