import fileinput
import sys


KEYBIND_REGMOD = '<item oor:path="/org.openoffice.Office.Accelerators/PrimaryKeys/Global"><node oor:name="{}" oor:op="replace"><prop oor:name="Command" oor:op="fuse"><value xml:lang="en-US">vnd.sun.star.script:Standard.o_ucsur.Main?language=Basic&amp;location=application</value></prop></node></item>'


def change_word(filepath: str, line_num: int, word: str, replace: str) -> None:
    for line in fileinput.input(filepath, inplace=True):
        if fileinput.filelineno() == line_num:
            line = line.replace(word, replace)
        sys.stdout.write(line)  # Prints to file, magic!


def add_line(filepath: str, line_num: int, contents: str) -> None:
    for line in fileinput.input(filepath, inplace=True):
        sys.stdout.write(line)
        if fileinput.filelineno() == line_num:
            sys.stdout.write(contents)


def convert_lo_keybind(keybind_raw: str, *, mac: bool=False) -> str:
    parts = keybind_raw.replace(" ", "").upper().split("+")
    key = parts.pop().upper()
    shift = "_SHIFT" if "SHIFT" in parts else ""
    mod1 = "_MOD1" if ("CMD" if mac else "CTRL") in parts else ""
    mod2 = "_MOD2" if "ALT" in parts else ""
    mod3 = "_MOD3" if mac and "CTRL" in parts else ""
    print(f"{key}{shift}{mod1}{mod2}{mod3}")
    return f"{key}{shift}{mod1}{mod2}{mod3}"


def add_lo_keybind(filepath: str,
                   line_num: int,
                   keybind_raw: str,
                   *,
                   mac: bool=False) -> None:
    keybind = convert_lo_keybind(keybind_raw, mac=mac)
    add_line(filepath, line_num, KEYBIND_REGMOD.format(keybind))


if __name__ == "__main__":
    globals()[sys.argv[1]](*[int(s) if s.isdigit() else s
                             for s in sys.argv[2:]])
