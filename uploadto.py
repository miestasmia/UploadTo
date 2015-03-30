####    SETTINGS    ####

IMGUR_CLIENT_ID     = ''
IMGUR_CLIENT_SECRET = ''

####      CODE      ####


import os
import sys

              # Windows                 Linux
if not (os.name == 'nt' or os.name == 'posix'):
    sys.exit("You're not on a supported OS")


import Tkinter, tkFileDialog
from imgurpython import ImgurClient
import pyperclip

import gtk.gdk
from PyQt4.QtCore import QRect
from PyQt4.QtGui import QPixmap, QApplication

import wx

app_wx = wx.App(False)
app_pyqt = QApplication(sys.argv)

# Get and check OS specific dependencies
if os.name == 'nt': # Windows
    from PIL import ImageGrab
elif os.name == 'posix':
    pass # TODO: Check if xclip is installed


def notif_sound():
    global app_wx
    wx.Sound('uploaded.wav').Play(wx.SOUND_SYNC)


# Read system args
args = sys.argv[1:]

# Define constants
SUPPORTED_IMAGE_TYPES = [
    ('All supported files', '*.jpg;*.jpeg;*.png;*.gif'),
    ('All files', '*.*')
]

# Create settings dictionary
settings = {}
valid_settings = {
    "--from": [
        "region",
        "window",
        "screen",
        "monitor",
        "clipboard",
        "file"
    ],
    "--to": [
       "imgur"
    ]
}
required_settings = set([
    "--from",
    "--to"
])

# Check for commands and save to settings
i = len(args)
while i > 0:
    i -= 2
    settings[args[i]] = args[i + 1]

for setting in settings:
    value = settings[setting]
    # Check if the argument exists
    if setting not in valid_settings:
        sys.exit("Argument \"" + setting + "\" is not recognized")
    # Check if the argument has a valid value
    if value not in valid_settings[setting]:
        sys.exit("Invalid value \"" + value + "\" for argument \"" + setting + "\"")

# Check if all the required settings are defined        
for required in required_settings:
    if not required in settings:
        sys.exit("Argument " + required + " is required");

# Create shorthand for --from and --to
arg_from = settings["--from"]
arg_to   = settings["--to"]

if arg_to == "imgur":
    client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)

cancelled = False

# Method for doing something with a file:
def doFile(path):
    global arg_to
    if arg_to == "imgur":
        global client
        url = client.upload_from_path(path, config = None, anon = True)['link']
    
    return url

        
# Obtain file from --from and call the doFile method, which satisfies --to
if arg_from == "file":
    root = Tkinter.Tk()
    root.withdraw()
    
    file = tkFileDialog.askopenfilename(
        filetypes = SUPPORTED_IMAGE_TYPES
    )
    
    if file != '':
        url = doFile(file)
    else:
        cancelled = True
elif arg_from == "clipboard":
    if os.name == 'nt': # Windows
        image = ImageGrab.grabclipboard()
        if not image == None:
            image.save('temp.png','PNG')
            url = doFile('temp.png')
            os.remove('temp.png')
        else:
            sys.exit("Your clipboard does not contain an image")
    elif os.name == 'posix': # Unix
        os.system("xclip -selection clipboard -t image/png -o > temp.png") # TODO: Error handling
        url = doFile('temp.png')
        os.remove('temp.png')
elif arg_from == "screen":
    # Get the default screen, containing all monitors
    screen = gtk.gdk.screen_get_default()
    screen_width  = screen.get_width()
    screen_height = screen.get_height()
    
    # Get all monitors on the screen
    monitors = []
    for m in range(screen.get_n_monitors()):
        monitors.append(screen.get_monitor_geometry(m))

    image = QPixmap.grabWindow(QApplication.desktop().winId(), -monitors[0].x, 0, screen_width, screen_height)    
    
    if(image != None):
        image.save('temp.png', 'png')
        url = doFile('temp.png')
        os.remove('temp.png')
    else:
        sys.exit("Unable to capture screen")
elif arg_from == "monitor":
    # Get the default screen, containing all monitors
    screen = gtk.gdk.screen_get_default()
    screen_width  = screen.get_width()
    screen_height = screen.get_height()
    
    # Get all monitors on the screen
    monitors = []
    for m in range(screen.get_n_monitors()):
        monitors.append(screen.get_monitor_geometry(m))
    
    # Pick the active monitor based on the cursor position (only cross-platform solution)
    rootwin = screen.get_root_window()
    cursor_x, cursor_y, cursor_mods =  rootwin.get_pointer()
    
    activeMonitor = None
    for m in monitors:
        if cursor_x in range(m.x, m.x + m.width):
            activeMonitor = m
            break
  
    
    image = QPixmap.grabWindow(QApplication.desktop().winId(), -monitors[0].x, 0, screen_width, screen_height)
    
    if(image != None):
        rect = QRect(activeMonitor.x, activeMonitor.y, activeMonitor.width, activeMonitor.height)
        image = image.copy(rect)
        
        image.save('temp.png', 'png')
        url = doFile('temp.png')
        os.remove('temp.png')
    else:
        sys.exit("Unable to capture screen")
else:
    print arg_from + " is not implemented yet."

if not cancelled:
    if arg_to == "imgur":
        pyperclip.copy(url)
        notif_sound()