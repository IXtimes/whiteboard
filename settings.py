import sys
import os

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    '''
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

COLOR_RANGE = ['0', '1', '2', '3', '4', '5','6', '7', '8', '9', 'A', 'B','C', 'D', 'E', 'F']
COLORS = (
	('000', '999', 'BBB','FFF'),
	('400', '900', 'B00','F00'),
	('040', '090', '0B0','0F0'),
	('004', '009', '00B','00F'),
	('F0F', 'FF0', '0FF','F66'),
	('94B', 'F90', '088','EAA'))
COLOR_COLS = len(COLORS[0])
COLOR_ROWS = len(COLORS)

# ui color 
CANVS_BG = '#f5f6ff'
BUTTON_COLOR = '#dbdbdb'
BUTTON_HOVER_COLOR = 'gray'
BUTTON_ACTIVE_COLOR = 'gray'
BRUSH_PREVIEW_BG = '#ebebeb'
SLIDER_RED = '#E00'
SLIDER_GREEN = '#0E0'
SLIDER_BLUE = '#00E'

