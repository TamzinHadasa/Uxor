SETLOCAL enabledelayedexpansion
ECHO "Runnning %date% %time%"
SET home=%~dp0
SET homeSrc=%home:\macros\LibreOffice\=%
SET helpers=%homeSrc%\setup_helpers.py
SET changeWord=python %helpers% change_word
SET LO=%AppData%\LibreOffice\4\user
SET xbaDir=%LO%\basic\Standard
SET xbaFile=o_ucsur.xba
SET pyDir=%LO%\Scripts\python
SET pyFile=o_ucsur.py
SET configFile=registrymodifications.xcu
SET tempFileName=.tempFile.txt


SET /p config=What config from configs.py should LibreOffice use? Leave^
 blank for default. || SET config=default
ECHO config is %config%

CD %xbaDir%
XCOPY /-I %home%\%xbaFile% .
IF NOT %config%==default (
    ECHO Changing config in .xba file to %config%
    RENAME %xbaFile% %tempFile%
    ECHO Renamed %xbaFile% to %tempFile%
    FOR /F "tokens=1-3*" %%i IN (%tempFile%) DO (
        ECHO %%k
        SET eye=%%i
        SET kay=%%k
        SET line=%%i %%j %%k %%l
        IF !eye!==config (
            SET line=%%i %%j "%config%"
        )
        ECHO !line! >> %xbaFile%
    )
    DEL %tempFile%
    ECHO Deleted %tempFile%
)

CD %pyDir%
XCOPY /-I %home%\%pyFile% .
ECHO Setting path in .py file to %homeSrc%
RENAME %pyFile% %tempFile%
ECHO Renamed %pyFile% to %tempFile%
FOR /F "tokens=1-3*" %%i IN (%tempFile%) DO (
    ECHO %%k
    SET eye=%%i
    SET kay=%%k
    SET line=%%i %%j %%k %%l
    IF !eye!==SRC_PATH (
        SET line=%%i %%j R"%homeSrc%"
    )
    ECHO !line! >> %pyFile%
)
DEL %tempFile%
ECHO Deleted %tempFile%

CD %LO%
FOR /F 