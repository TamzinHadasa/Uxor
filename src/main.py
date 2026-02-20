__author__ = "Tamzin Hadasa Kelly"
__email__ = "coding@tamz.in"
__copyright__ = "Copyright 2026 Tamzin Hadasa Kelly"
__license__ = "The MIT License"
__version__ = "2.0.0"
import sys

# This loads the default Uxor implementation.  To use a different version,
# change `default` to the name of that version as appears in configs.py.
from configs import default as uxor


# Extra layer of abstraction for import by LibreOffice.
def main(input_):
    return uxor.convert(input_)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(main("".join(sys.argv[1:])))
    else:
        while True:
            try:
                print(main(input("> ")))
            except ValueError as e:
                print(f"ERROR. Invalid sequence {e.args[0]}\n> ")