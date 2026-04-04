# Enables Uxor in LibreOffice.  See Uxor's readme for more information.
import sys

# CHANGE THIS to the filepath to the /src subdirectory of where you've
# installed Uxor.  The "R" is there to avoid backspace issues with 
# Windows filepaths.
SRC_PATH = "REPLACEME"
sys.path.append(SRC_PATH)

from configs import *
