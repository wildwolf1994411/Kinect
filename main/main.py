from .klib import bodygame3
from .klib import msgbox
from .klib import welcome
import wx, pdb
# __main__ = "Kinect v2 Body Analysis"
def main():
    info = None
    app = wx.App()
    while not (hasattr(info, 'name') and hasattr(info, 'age') and hasattr(info, 'gender')):
        info = msgbox.Msgbox(None, title="Welcome")
        app.MainLoop()

    main_win = welcome.Welcome_win(info, parent=None, title='Menu')
    app.MainLoop()
    return main_win.game