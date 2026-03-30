# Enables Uxor in LibreOffice.  See Uxor's readme for more information.
import sys

# CHANGE THIS to the filepath to the /src subdirectory of where you've
# installed Uxor.  The "R" is there to avoid backspace issues with 
# Windows filepaths.
sys.path.append(R'/path/to/your/directory/')

from configs import *  # type: ignore # pylint: disable=import-error,wildcard-import,wrong-import-position
