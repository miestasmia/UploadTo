####    SETTINGS    ####

IMGUR_CLIENT_ID     = ''
IMGUR_CLIENT_SECRET = ''

####      CODE      ####


import os
import sys
import Tkinter, tkFileDialog
from imgurpython import ImgurClient
import pyperclip
import winsound
from PIL import ImageGrab

def notif_sound():
    winsound.PlaySound('uploaded.wav', winsound.SND_FILENAME)


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
    if arg_to == "imgur":
        global client
        url = client.upload_from_path(path, config = None, anon = True)['link']
    
    return url

        
# Obtain file and call the doFile method

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
    image = ImageGrab.grabclipboard()
    
    if not image == None:
        image.save('temp.png','PNG')
        url = doFile('temp.png')
        os.remove('temp.png')
    else:
        sys.exit("Your clipboard does not contain an image")
else:
    print arg_from + " is not implemented yet."

if not cancelled:
    if arg_to == "imgur":
        pyperclip.copy(url)
        notif_sound()