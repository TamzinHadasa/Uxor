import sys

# This loads the default Uxor implementation.  To use a different version,
# change `default` to the name of that version as appears in configs.py.
from configs import default as uxor

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(uxor.convert(sys.argv[1]))
    else:
        while True:
            try:
                print(uxor.convert(input("> ")))
            except ValueError as e:
                print(f"ERROR. Invalid sequence {e.args[0]}\n> ")