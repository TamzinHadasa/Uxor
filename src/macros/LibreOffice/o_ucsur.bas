REM  *****  BASIC  *****
REM See readme.md for instructions on adding this to LibreOffice.
Option Explicit

Sub Main
Dim sp As Object ' com.sun.star.script.provider.XScriptProvider compatible
Dim uri As String
dim getUcsur as object
sp = ThisComponent.getScriptProvider()
REM Change the bit between $ and ? to use a different Uxor object from config.py!
uri = "vnd.sun.star.script:o_ucsur.py$default?language=Python&location=share"
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