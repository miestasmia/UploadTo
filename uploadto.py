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
from Tkinter import *
from imgurpython import ImgurClient
import pyperclip

from PIL import Image, ImageTk

import gtk.gdk
from PyQt4.QtCore import QRect
from PyQt4.QtGui import QPixmap, QApplication

import wx

app_wx = wx.App(False)
app_pyqt = QApplication(sys.argv)

# Get and check OS specific dependencies
if os.name == 'nt': # Windows
    from PIL import ImageGrab
elif os.name == 'posix': # Linux
    if os.system("which xclip") == 1:
        sys.exit("You don't have xclip installed")


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
elif arg_from == 'region':
    # Get the default screen, containing all monitors and its width
    screen = gtk.gdk.screen_get_default()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Get all monitors on the screen
    monitors = []
    for m in range(screen.get_n_monitors()):
        monitors.append(screen.get_monitor_geometry(m))
    
    # Take a fullscreen screenshot and save it to temp.png
    image = QPixmap.grabWindow(QApplication.desktop().winId(), -monitors[0].x, 0, screen_width, screen_height)
    image.save('temp.png', 'png')
    
    # Create a region overlay window using Tkinter
    region = Tk()
    region.resizable(width = False, height = False)
    
    geometry = '%dx%d+%d+%d' % (screen_width, screen_height, -monitors[0].x, -monitors[0].y)
    region.geometry(geometry)
    
    region.overrideredirect(1) # Borderless
    
    region.config(cursor = "crosshair")
    
    # Create the canvas to draw on
    canvas = Canvas(region, width = screen_width, height = screen_height)
    canvas.pack()
    
    # Put the screenshot as the background
    im = Image.open('temp.png')
    tkimage = ImageTk.PhotoImage(im)
    canvas.create_image(0, 0, image = tkimage, anchor = NW)
    
    # Create the rectangle that'll later be moved
    rectangle = canvas.create_rectangle(0, 0, 0, 0, dash = (3, 5))
    
    # Save the drag and drop coords
    start_x = None
    start_y = None
    mouse_x = 0
    mouse_y = 0
    
    # Define url
    url = ""
    
    def region_button1_down(event):
        global start_x
        global start_y
        start_x = event.x
        start_y = event.y
        
    def region_button1_up(event):
        global image, url
        region.destroy()
        
        # Crop the image to fit the rectangle
        
        x1 = start_x
        y1 = start_y
        x2 = event.x
        y2 = event.y
        
        # Swap x and y if x2, y2 are smaller than y1, y1
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        
        width = x2 - x1
        height = y2 - y1
        
        rect = QRect(
            x1,
            y1,
            width,
            height
        )
        image = image.copy(rect)
        image.save('temp.png', 'png')
        url = doFile('temp.png')
        os.remove('temp.png')
        
    def region_motion(event):
        global mouse_x
        global mouse_y
        mouse_x = event.x
        mouse_y = event.y
    
    def region_draw():
        if not start_x == None:
            canvas.coords(rectangle, start_x, start_y, mouse_x, mouse_y)
        
        region.after(15, region_draw)
    
    region.bind("<Button-1>", region_button1_down)
    region.bind("<ButtonRelease-1>", region_button1_up)
    region.bind("<Motion>", region_motion)
    region.after(15, region_draw)
    
    region.mainloop()
    

if not cancelled:
    if arg_to == "imgur":
        pyperclip.copy(url)
        notif_sound()