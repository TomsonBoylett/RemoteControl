import re
import logging
import sys
import shlex
import subprocess
import os

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import PlainTextResponse
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn
import pyautogui
import toml

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

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
key_pattern = re.compile(r'{(' + key_pattern + r')}|[ -~]', re.IGNORECASE)

class CommandError(Exception):
    pass

def press_hotkey(keys):
    tokens = list(key_pattern.finditer(keys))

    # Make sure entire string is matched
    if sum(t.end() - t.start() for t in tokens) != len(keys):
        raise CommandError(f'Invalid hotkey: {keys}')

    tokens = [t.group() for t in tokens]
    keys = [t[1:-1] if t[0] == '{' else t for t in tokens]

    pyautogui.hotkey(*keys)
    
    LOGGER.debug(f'Executed Hotkey: {keys}')

def launch_program(program):
    try:
        args = shlex.split(program)
        subprocess.Popen(args)
    except KeyError as e:
        raise CommandError(f'Invalid program {str(e)}')

ws_commands = {
    'k': press_hotkey,
    'l': launch_program
}

class RemoteControl(WebSocketEndpoint):
    encoding = "text"

    async def on_receive(self, websocket, data):
        try:
            page, item_index = data.split(',')
            command = config['pages'][page][int(item_index)]['command']
            ws_commands[command[0]](command[1:])
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

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    uvicorn.run(app, host=config['bind_address'], port=config['port'])