# UploadTo
A simplistic screenshot tool focused on easy modability.

**Please note:** This project has officially been abandoned. Refer to [Perdyshot](https://github.com/Miestasmia/Perdyshot) for the maintained successor.

# Usage
Navigate to the directory UploadTo is in, and run ```python uploadto.py``` with any arguments you may want.

## Arguments
| Name         | Description                            | Valid values                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Required   |
| ------------ | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| ``--from`` | The source from which to get the image | <samp title="Lets you select a region with a crosshair and a rectangle on the entire screen">```region```</samp>, <samp title="Takes a screenshot of your entire screen, consisting of all your monitors">```screen```</samp>, <samp title="Takes a screenshot of the monitor your cursor is currently on">```monitor```</samp>, <samp title="Uses the image currently in your clipboard">```clipboard```</samp>, <samp title="Opens a pick file dialog">```file```</samp> | *required* |
| ```--to```   | What to do with the image              | <samp title="Uploads the image to imgur">```imgur```</samp>                                                                                                                                                                                                                                                                                                                                                                                                                | *required* |

# Installation
Please note that UploadTo is still in Alpha and *will* have bugs and issues.

UploadTo was developed on a Windows computer with cross-platform compatibility in mind. It should work on the majority of Linux distros and OSX (untested).

1. Clone this repo in git, or download the master as a zip or tarball and unzip it somewhere on your computer.
2. Make sure you have Python installed. I coded this using Python 2.7 x32, but it should work with most other win32 versions. Please note that it only works on Python win32, and that you can run Python win32 just fine on a 64 bit computer. If you experience issues, try install Python 2.7 x32 and make it run with that install.
3. Install all the requirements, if you don't have them already. [List of requirements.](#requirements)
4. (Optional) [Set up hotkeys.](#hotkeys)

## Requirements
### Windows
1. Make sure you have pip installed. Open a command line (```cmd``` in a run dialog or search window) and run ```where pip```. If the result is just a path like ```c:\Python27\Scripts\pip.exe``` then you already have it installed. If not, download [get-pip.py](https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py) and simply run ```python get-pip.py``` in the directory you saved it in. You may need to run it from an elevated command prompt (right click on ```cmd.exe``` and choose "Run as administrator")
2. [Install the all-in-one GTK+ bundle.](http://www.gtk.org/download/win32.php)
3. [Install PyQt4.](http://www.riverbankcomputing.co.uk/software/pyqt/download)
4. [Install wxPython.](http://www.wxpython.org/download.php)
5. Run the following commands in command prompt:
	* ```pip install imgurpython```
	* ```pip install pyperclip```
	* ```pip install PIL```
	* ```pip install pygtk```
6. [Register for the imgur API](https://api.imgur.com/oauth2/addclient)
7. Update ```uploadto.py``` with your API credentials.

### Linux
1. Make sure you have pip installed. Open a shell window (usually <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>) and run ```which pip```. If the result isn't a path, you don't have it installed. To install it, install ```python-pip``` with your favorite package manager:
	* ```sudo apt-get install python-pip```
	* ```sudo yum install python-pip```
	* ```sudo pacman -S python-pip```
2. Install PyQt4 with your favorite package manager:
	* ```sudo apt-get install python-qt4```
	* ```sudo yum install python-qt4```
	* ```sudo pacman -S python-qt4```
3. Install wxPython with your favorite package manager:
	* ```sudo apt-get install python-wxgtk2.8```
	* ```sudo yum install python-wxgtk2.8```
	* ```sudo pacman -S install python-wxgtk2.8```
4. Install xclip with your favorite package manager:
	* ```sudo apt-get install xclip```
	* ```sudo yum install xclip```
	* ```sudo pacman -S xclip```
5. Run the following commands:
	* ```pip install imgurpython```
	* ```pip install pyperclip```
	* ```pip install PIL```
	* ```pip install pygtk```
6. [Register for the imgur API](https://api.imgur.com/oauth2/addclient)
7. Update ```uploadto.py``` with your API credentials.
	

## Hotkeys
### Windows
1. Create a directory to store the shortcuts in.
2. In the directory create a new shortcut (right click &rarr; New &rarr; Shortcut).
3. Put ```python path/to/uploadto.py``` in the input field and add the [arguments](#arguments) you want.
4. Name the shortcut something appropriate (e.g. region if this is the region shortcut).
5. Right click on the shortcut &rarr; Properties.
6. Pick a shortcut key and set Run to Minimized.
7. Repeat steps 2 &ndash; 7 until you have all the hotkeys you want.

**Please note that Windows has a known bug that causes these hotkeys to sometimes stop working.**

### Linux
[Follow this handy guide by MakeTechEasier](http://www.maketecheasier.com/autokey-make-your-own-keyboard-shortcuts-in-linux/).

Since you're using Linux, you should know how to set this up.

# TODO
* Create a GUI mode
* Create an installer that automatically installs all dependencies (or as many as legally allowed)
* Optimize the speed (region is ridiculously slow)
* Add a ```--from window``` that captures the active window. [Currently waiting for this StackOverflow question to get answered.](http://stackoverflow.com/questions/29355898/getting-the-active-root-window-using-gtk-gdk-in-python)
* Add an <kbd>Esc</kbd> to cancel region select, and right click to select new rectangle.
* Add support for more more image hosts other than imgur.
* Add an export to file mode with custom string formatting
* Add a ```--no-sound```.
* Add a ```--print-url``` that prints the URL instead of copying it to the user's clipboard.

















