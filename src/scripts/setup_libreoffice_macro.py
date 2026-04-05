import fileinput
import os
from pathlib import Path
import shutil
import sys


THIS_DIR = Path(os.path.realpath(__file__)).parent.parent.parent.absolute()
SRC_DIR = f"{THIS_DIR}/src"
PIP_SOURCE = "https://bootstrap.pypa.io/get-pip.py"
LO_PROGRAM_DIR = "C:/Program Files/LibreOffice"
APPDATA = os.getenv('APPDATA')
LO_APPDATA_DIR = f"{APPDATA}/LibreOffice/4/user"
XBA_DIR = f"{LO_APPDATA_DIR}/basic/Standard"
PY_DIR = f"{LO_APPDATA_DIR}/Scripts/python"
SCRIPT_NAME = "o_ucsur"

CONFIG_PROMPT = "What config from configs.py should LibreOffice use? Leave blank for default.\n> "
XBA_TEMPLATE = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="{SCRIPT_NAME}" script:language="StarBasic">REM  *****  BASIC  *****
REM See readme.md for instructions on adding this to LibreOffice.
Option Explicit

Sub Main
dim sp As Object ' com.sun.star.script.provider.XScriptProvider compatible
dim config as String
dim uri As String
dim getUcsur as object
sp = ThisComponent.getScriptProvider()
REM Change this to use a different Uxor object from configs.py!
uri = "vnd.sun.star.script:{SCRIPT_NAME}.py${{config}}?language=Python&location=share"
set getUcsur = sp.getScript(uri)
REM ----
dim currSel as string
dim frame as object
dim dispatcher as object
dim ucsur as string
currSel = ThisComponent.getCurrentSelection().getByIndex(0).String
frame = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")
ucsur = getUcsur.invoke(Array(currSel), Array(), Array())
dim args1(0) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Text"
args1(0).Value = ucsur
dispatcher.executeDispatch(frame, ".uno:ResetAttributes", "", 0, Array())
dispatcher.executeDispatch(frame, ".uno:InsertText", "", 0, args1())
End Sub
</script:module>"""

PY_CONTENTS = f"""import sys
sys.path.append(R"{SRC_DIR}")
from configs import *
"""

KEYBIND_RAW_DEFAULT = "alt+u"
KEYBIND_RAW_PROMPT = f"What keybind do you want to use to run the script? Leave blank for default ({KEYBIND_RAW_DEFAULT}). To see options, go to Tools>Customize in LibreOffice and enter a value exactly as shown in the left column there.\n> "
KEYBIND_REGMOD_TEMPLATE = f'<item oor:path="/org.openoffice.Office.Accelerators/PrimaryKeys/Global"><node oor:name="{{keybind}}" oor:op="replace"><prop oor:name="Command" oor:op="fuse"><value xml:lang="en-US">vnd.sun.star.script:Standard.{SCRIPT_NAME}.Main?language=Basic&amp;location=application</value></prop></node></item>'


def make_xba():
    config = input(CONFIG_PROMPT) or "default"
    xba_contents = XBA_TEMPLATE.format(config=config)
    print("Making BASIC script")
    with open(f"{XBA_DIR}/o_ucsur.xba", "w") as f:
        f.write(xba_contents)


def make_py():
    print("Making Python script to connect BASIC file to Uxor")
    with open(f"{PY_DIR}/o_ucsur.py", "w") as f:
        f.write(PY_CONTENTS)
    

def make_keybind() -> None:
    keybind_raw = input(KEYBIND_RAW_PROMPT) or KEYBIND_RAW_DEFAULT
    keybind = convert_keybind(keybind_raw)
    regmod = KEYBIND_REGMOD_TEMPLATE.format(keybind=keybind)
    print("Adding keybind to registry")
    add_line(f"{LO_APPDATA_DIR}/registrymodifications.xcu", 2, regmod)


def convert_keybind(keybind_raw: str, *, mac: bool=False) -> str:
    parts = keybind_raw.replace(" ", "").upper().split("+")
    key = parts.pop().upper()
    shift = "_SHIFT" if "SHIFT" in parts else ""
    mod1 = "_MOD1" if ("CMD" if mac else "CTRL") in parts else ""
    mod2 = "_MOD2" if "ALT" in parts else ""
    mod3 = "_MOD3" if mac and "CTRL" in parts else ""
    print(f"{key}{shift}{mod1}{mod2}{mod3}")
    return f"{key}{shift}{mod1}{mod2}{mod3}"


def add_line(filepath: str, line_num: int, new_line: str) -> None:
    for line in fileinput.input(filepath, inplace=True):
        sys.stdout.write(line)  # Prints to file.  Magic!
        if fileinput.filelineno() == line_num and line != new_line:
            sys.stdout.write(new_line)


if __name__ == "__main__":
    # make_xba()
    # make_py()
    # make_keybind()
    install_uxor_in_lo()
