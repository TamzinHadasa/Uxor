ECHO "Runnning %date% %time%"
SET home=%~dp0
SET templates=%home%templates
SET homeSrc=%home:\macros\LibreOffice\=%
SET helpers=%homeSrc%\setup_helpers.py
SET LO=%AppData%\LibreOffice\4\user
SET xbaDir=%LO%\basic\Standard
SET xbaFile=o_ucsur.xba
SET pyDir=%LO%\Scripts\python
SET pyFile=o_ucsur.py
SET configFile=registrymodifications.xcu

SET /p config=What config from configs.py should LibreOffice use? Leave^
 blank for default. || SET config=default

CD %xbaDir%
XCOPY /-I /Y %templates%\%xbaFile% .
ECHO Setting config to %config%
PYTHON %helpers% change_word %xbaFile% 12 default %config%

CD %pyDir%
XCOPY /-I /Y %templates%\%pyFile% .
ECHO Setting path in .py file to %homeSrc%
PYTHON %helpers% change_word %pyFile% 7 REPLACEME %homeSrc%

CD %LO%
SET /p keybind=What keybind do you want to use to run the script? Leave^
 blank for default (alt+u). To see options, go to Tools^>Customize in^
 LibreOffice and enter a value exactly as shown in the left column ^
 there. || SET keybind=alt+u
PYTHON %helpers% add_lo_keybind %configFile% 2 %keybind%
