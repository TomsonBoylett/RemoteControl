import logging
import webbrowser

import wx
import wx.adv
import toml

from util import resource_path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config = toml.load('config.toml')

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, iconType=wx.adv.TBI_DEFAULT_TYPE):
        super().__init__(iconType=iconType)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
    
    def on_left_down(self, event):
        protocol = 'https' if config['ssl_enabled'] else 'http'
        port = config['port']
        webbrowser.open(f'{protocol}://127.0.0.1:{port}')

gui = wx.App()
tray_icon = TaskBarIcon()
tray_icon.SetIcon(wx.Icon(resource_path('icon/icon-128.ico')))

def run_app():
    gui.MainLoop()

if __name__ == '__main__':
    gui.MainLoop()