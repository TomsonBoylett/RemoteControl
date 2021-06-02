import re
import logging
import sys

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn
import pyautogui

import config

LOGGER = logging.getLogger(__name__)

templates = Jinja2Templates(directory='templates')
key_pattern = re.compile(r'^({enter}|{backspace}|[ -~])$', re.IGNORECASE)

class CommandError(Exception):
    pass

def press_key(key):
    if not key_pattern.match(key):
        raise CommandError(f'Invalid key: {key}')
    
    if key[0] != '{':
        pyautogui.write(key)
    else:
        key = key[1:-1]
        pyautogui.press(key)
    
    LOGGER.debug(f'Key: {key}')

ws_commands = {
    'k': press_key
}

class RemoteControl(WebSocketEndpoint):
    encoding = "text"

    async def on_receive(self, websocket, data):
        try:
            ws_commands[data[0]](data[1:])
        except KeyError as e:
            await websocket.send_text(f'Invalid command {str(e)}')
        except CommandError as e:
            await websocket.send_text(str(e))

async def homepage(request):
    return templates.TemplateResponse('index.html.jinja', {
        'columns': config.COLUMNS,
        'rows': config.ROWS,
        'items': config.ITEMS,
        'request': request
    })

async def css(request):
    return templates.TemplateResponse('main.css.jinja', media_type='text/css', context={
        'columns': config.COLUMNS,
        'rows': config.ROWS,
        'request': request
    })

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/main.css', css),
    Mount('/static', app=StaticFiles(directory='static'), name='static'),
    WebSocketRoute('/ws', RemoteControl)
])

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    uvicorn.run(app, host='0.0.0.0', port=8000)