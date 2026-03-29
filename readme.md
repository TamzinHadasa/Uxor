# Uxor: toki pona's Universal(ish) TRANScriber tO ucsuR

A number of input methods exist for writing *sitelen pona* using UCSUR
codepoints.  See generally <https://sona.pona.la/wiki/Input_methods> and
<https://github.com/neroist/sitelen-pona-ucsur-guide?tab=readme-ov-file#input>.
However, almost all of these methods suffer from being limited to particular
operating systems.  Furthermore, many are not configurable to handle the variety
of syntaxes used in the not-yet-quite-standardized ecosystem of sitelen pona
fonts.  Meanwhile, Latin-ligature-based fonts are not well-suited for production
usage.

The only almost-entirely-foolproof strategy, therefore, is to write things in
Latin characters and then convert them as one goes along.  Several Web
implementations have been made of this, including <https://linku.la/tools?q=>.
However, there are obvious workflow issues with this approach, and still little
to no configurability.

I wrote the initial version of this code while normalizing the style of a
manuscript that had wound up using a mix of UCSUR, spaced Latin ligatures, and
unspaced Latin ligatures.  My initial goal was just to tidy up what I'd already
written, but I realized upon concluding that that I'd made something far more
powerful: a lightweight tool that can be plugged into almost any software,
allowing users to write things in Latin characters and then quickly convert to
UCSUR without having to interrupt their workflow.

## Installation

I'll try to be very detailed here because I'm sick of reading documentation that
assumes that, just because someone wants to download software, they know things
like what a command line is or how to use Git.  If you already know these
things, good for you; why are you reading this section?  Just do the things.

You can download this repo as a .zip file by clicking the green "Code" button
at the top of the GitHub page.  (Are you not currently on the GitHub page?  See
<https://github.com/TamzinHadasa/Uxor>).  Then you can do all the things
described below with the code that you download.  You'll need Python installed;
if you don't have that please see <https://www.python.org/downloads/>, v3.11.2 
or higher.

Better yet, though, clone this as a Git repository.  Then you can easily update
it if I make changes.  Create a folder that you'd like to clone the code to.  
Get Git at <https://git-scm.com/install/> if you don't have it.  If you're using 
a program like VS Code <https://code.visualstudio.com/download>, there should be 
commands to clone `https://github.com/TamzinHadasa/Uxor.git`. If not, open the 
command line on your device—if you don't know how to do this, Google 
`open command line` and your operating system name—change directory to the 
folder you just made (on most OSes this will be `cd ` and the path to the file),
and enter the following:
```sh
git clone https://github.com/TamzinHadasa/Uxor.git
```

## Universal behavior

Uxor runs its input through a Python class called `Uxor`.  When parsing input,
any `Uxor` object will first try to convert strings to UCSUR using a lookup
table, and if that fails will see if the string is itself a valid value in that
table, and if that fails will make its best effort at seeing if unspaced
substrings can be parsed using those first two approaches.  It is able to modify
the input text both before and after the conversions using [regexes](https://www.regular-expressions.info/),
although by default it does not do so.

## Default settings

The default `Uxor` object uses the following settings:
* It uses all UCSUR codepoints for sitelen pona, plus 「, 」, and the zero-width
  joiner (U+200D).
* It assumes the sequence for adding a variant to a glyph is merely appending a
  numeral.
* It does *not* modify the input before separating it.
* It assumes that all sequences of whitespace (spaces, newlines, etc.) should be
  reduced to a single space.
* It assumes that a single space should be used to divide words.  (As noted, it
  still does its best to find words in unspaced sequences if otherwise
  unresolvable.)
* It does *not* modify the output after doing its conversions.

## Custom settings

*All* of the above assumptions can be changed.  To make a custom `Uxor` object,
open `configs.py` in the directory you downloaded or cloned this code to.  See
the documentation there for more information.

Adding a new `Uxor` object to that file will not automatically enable it.
Instead, open `o_ucsur.py` and, in the import command, change `default` to the 
name of your object.

## As a command-line tool

The `o_ucsur` command can be accessed from the command line by writing `python3`
and the filepath you've installed `o_ucsur.py` at.  If you enter this on its
own, it will open an interactive dialog where you can input multiple strings.
Alternately, you can include your string directly in the command, e.g.
`python3 o_ucsur.py ali li pona`. (Syntax assumes you are currently in the
directory where you installed the code.)

## As a macro

Different platforms have a wide variety of methods to bind a command to a
hotkey.  You'll need to find the one that works best for your use case.
Specifically, you will want something that lets you see what text is currently
highlighted, run arbitrary code on it, and then "type" that code's output.

Some platforms may have dedicated ways to run Python code from within a hotkey
scripting service.  If not, as long as they have some way to run a shell
command, you can execute
```sh
python3 full/filepath/to/o_ucsur.py SELECTED_TEXT
```
replacing `SELECTED_TEXT` with whatever variable represents the text currently
highlighted.

### LibreOffice macro

I have created a fully functional macro that does just this in LibreOffice, at
[`macros/LibreOffice/o_ocsur.bas`](src/macros/LibreOffice/o_ocsur.bas).

To enable it, you must first add [`macros/LibreOffice/import_o_ocsur.py`](src/macros/LibreOffice/import_o_ocsur.py)
to the `share` directory of your LibreOffice installation.  On Linux this will
likely be `/lib/libreoffice/share/Scripts/python`. So from Uxor's directory you
can run:
```sh
sudo cp macros/LibreOffice/o_ucsur.py /lib/libreoffice/share/Scripts/python/
```
Then: 
* Open LibreOffice
* `Tools > Macros > Edit Macros`
* `File > Import BASIC`
* Copy the source code of [`macros/LibreOffice/o_ocsur.bas`](src/macros/LibreOffice/o_ocsur.bas) 
  into a the macro code editor.  (This is faster and less error-prone than
  using the import dialog.)
* In line 11, if you do not want to be using the default `Uxor` instance, change
  the word after the dollar sign to the name of your preferred instance.
* `File > Save`
* `Tools > Organize Macros > Basic`
* [Optional] Give the macro a descriptive name:
  * `My Macros > Standard > Module1` (or whatever name LO has assigned)
  * `Organizer` button on right side
  * Double click the macro's name; type a new name; press `enter`
  * Close the frontmost window
* Back in the first organizer window, with the macro selected, click `Assign`
* Go to the `Keyboard` tab; select the `LibreOffice` radio button on the right
* Scroll to `Alt+U`
* In the `Category` dialog below, scroll to `Application Macros > My Macros > Standard`
  and select the macro's name. "Main" will now appear in the `Function` dialog
  to the right.
* Click `Modify` above.

This approach dynamically imports the version of Uxor you have copied/cloned.
Changes to that version may sometimes not take immediate effect in LibreOffice;
try restarting the program if so.

You can change freely between multiple `Uxor` instances by modifying line 11 of
the macro (without needing to restart), or can even make separate macros with
different keybinds for different instances.

The LibreOffice script does not pay attention to what `Uxor` instance is
currently selected in [`main.py`](src/main.py).

## Contributing

Pull requests welcome! In particular, if you create a macro for a new scripting
platform, I will happily add it to the [`macros`](src/macros) directory.

## Conclusion

In addition to its silly backronym, and to sounding like the way I personally
pronounce "UCSUR", "uxor" is Latin for "spouse", that it may serve as a
faithful companion to you in your sitelen pona efforts. Generalizing that
translation to a more *pona* reckoning of relationships, I dedicate this 
project *tawa olin mi Kelisen, tawa olin mi Apike, tawa olin mi Juli*.