#!/usr/bin/env python

"""
Make this script your default browser in order to
choose which browser to use when opening a URI. Make sure to pass
the URI to the script via the "%s" variable.
"""

import wx
import os, sys

# Set the URI to the first command line argument (if given):
if len(sys.argv) > 1:
    uri = sys.argv[1]
else:
    uri = ''

def which(program):
    """
    Attempt to expand the path of a specified executable.
    """

    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

# Check whether certain common browsers are present:
possible_browsers = {'Chromium': 'chromium-browser',
                     'Epiphany': 'epiphany',
                     'Firefox': 'firefox',
                     'Konqueror': 'konqueror',
                     'Midori': 'midori',
                     'Opera': 'opera'}

browsers = {}
for browser in possible_browsers:
    name = possible_browsers[browser]
    full_path = which(name)
    if full_path:
        browsers[browser] = (name, full_path)
    
class AppFrame(wx.Frame):
    def __init__(self, parent, id, title):

        N = len(browsers.keys())

        # Prevent the frame from being resized:
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition,
                          wx.Size(80*N, 80),
                          style=wx.FRAME_TOOL_WINDOW | wx.RESIZE_BORDER)
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridSizer(1, N, 2, 2)
        
        # Dict to map button ids to browser commands:
        self.button_to_browser = {}
        for browser in browsers.keys():
            name, full_path = browsers[browser]

            icon = wx.ArtProvider.GetIcon(name, wx.ART_OTHER, 
                                          (64, 64))
            bmp = wx.BitmapFromIcon(icon)
            button = wx.BitmapButton(panel, -1, bmp, style=wx.NO_BORDER)
            button.SetToolTipString(browser)

            # button = wx.Button(self, -1, browser)
            grid.Add(button, 0, wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.OnClick, button)
            self.button_to_browser[button.Id] = full_path
        sizer.Add(grid, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT | wx.RIGHT, 2)
        panel.SetSizer(sizer)
        self.Centre()

        # Focus on the panel to catch keystrokes:
        panel.SetFocusIgnoringChildren()

        # Exit if the ESC key is pressed:
        panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)       

    def OnClick(self, event):

        # The first parameter is the name to give to the executed
        # process:
        os.execl(self.button_to_browser[event.Id], '', uri)

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Close()
            
class App(wx.App):
    def OnInit(self):

        # Exit if no browsers are found:
        if len(browsers) == 0:
            wx.MessageBox('No browsers found', 'Chooser Error')
            sys.exit(1)
        frame = AppFrame(None, -1, 'Select a Browser')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
    
app = App(0)
app.MainLoop()
