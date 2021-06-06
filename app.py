import re
import logging
import sys
import subprocess
import os
import csv
import threading

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import PlainTextResponse
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn
import pyautogui
import toml
import PIL
import pystray

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
log_handler = logging.handlers.RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=2)
log_handler.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('[%(asctime)s]    %(name)s    %(levelname)s   %(message)s')
log_handler.setFormatter(log_formatter)
root_logger.addHandler(log_handler)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

config = toml.load('config.toml')

templates = Jinja2Templates(directory=resource_path('templates'))
key_pattern = '|'.join(re.escape(k) for k in pyautogui.KEY_NAMES)
key_pattern = re.compile(r'{(' + key_pattern + r')}|([ -~])', re.IGNORECASE)

class CommandError(Exception):
    pass

def press_hotkey(keys):
    tokens = list(key_pattern.finditer(keys))

    # Make sure entire string is matched
    if sum(t.end() - t.start() for t in tokens) != len(keys):
        raise CommandError(f'Invalid hotkey: {keys}')

    keys = [t.group(1) if t.group(1) else t.group(2) for t in tokens]

    pyautogui.hotkey(*keys)
    
    logger.debug(f'Executed Hotkey: {keys}')

def launch_program(*args):
    try:
        subprocess.Popen(args)
        logger.debug(f'Launched program: {args}')
    except KeyError as e:
        raise CommandError(f'Invalid program {str(e)}')

ws_commands = {
    'hotkey': press_hotkey,
    'launch': launch_program
}

class RemoteControl(WebSocketEndpoint):
    encoding = "text"

    async def on_receive(self, websocket, data):
        try:
            logger.debug(f'Received data from websocket: {data}')
            raw_command = next(csv.reader([data]))
            page = raw_command[0]
            item_index = int(raw_command[1])
            item_config = config['pages'][page][item_index]

            if item_config.get('keyboard', False):
                command = 'hotkey'
                args = raw_command[2:]
            else:
                command = item_config['command'][0]
                args = item_config['command'][1:]

            ws_commands[command](*args)
        except (KeyError, IndexError, ValueError) as e:
            await websocket.send_text(f'Invalid command: {str(e)}')
        except CommandError as e:
            await websocket.send_text(str(e))

async def homepage(request):
    page = request.path_params.get('page', 'Main')

    if page not in config['pages']:
        return PlainTextResponse("Not Found", status_code=404)

    return templates.TemplateResponse('index.html.jinja', {
        'columns': config['columns'],
        'rows': config['rows'],
        'page':  page,
        'items': config['pages'][page],
        'request': request
    })

async def css(request):
    return templates.TemplateResponse('main.css.jinja', media_type='text/css', context={
        'columns': config['columns'],
        'rows': config['rows'],
        'request': request
    })

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/page/{page}', homepage),
    Route('/main.css', css),
    Mount('/static', app=StaticFiles(directory=resource_path('static')), name='static'),
    WebSocketRoute('/ws', RemoteControl)
])

logging.basicConfig(stream=sys.stdout)
uvi_args = {
    'host': config['bind_address'],
    'port': config['port'],
}
if config['ssl_enabled']:
    uvi_args.update({
        'ssl_keyfile': config['ssl_keyfile'],
        'ssl_certfile': config['ssl_certfile']
    })
t = threading.Thread(target=uvicorn.run,
                     args=(app,),
                     kwargs=uvi_args,
                     daemon=True)
t.start()

icon = pystray.Icon('Remote Control')
with PIL.Image.open(resource_path("icon/icon-128.ico")) as im:
    im.load()
    icon.icon = im
icon.menu = pystray.Menu(
    pystray.MenuItem('Exit', lambda icon: icon.stop())
)
icon.run()