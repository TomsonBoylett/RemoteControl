import csv
import base64
import binascii
import logging
import toml

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import PlainTextResponse
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser,
    AuthCredentials, requires
)
import uvicorn

from util import resource_path
from commands import COMMANDS, CommandError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config = toml.load('config.toml')

templates = Jinja2Templates(directory=resource_path('templates'))

class RemoteControl(WebSocketEndpoint):
    encoding = "text"

    @requires('authenticated')
    async def on_receive(self, websocket, data):
        try:
            logger.debug(f'Received data from websocket: {data}')

            raw_command = next(csv.reader([data]))
            page = raw_command[0]
            item_index = int(raw_command[1])

            item_config = config['pages'][page][item_index]

            if item_config.get('keyboard', False):
                command = 'keyboard'
                args = raw_command[2:]
            else:
                command = item_config['command'][0]
                args = item_config['command'][1:]

            COMMANDS[command](*args)
        except (KeyError, IndexError, ValueError) as e:
            await websocket.send_text(f'Invalid command: {str(e)}')
        except CommandError as e:
            await websocket.send_text(str(e))

@requires('authenticated')
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

@requires('authenticated')
async def css(request):
    return templates.TemplateResponse('main.css.jinja', media_type='text/css', context={
        'columns': config['columns'],
        'rows': config['rows'],
        'request': request
    })

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if not config['auth_enabled']:
            return AuthCredentials(["authenticated"]), SimpleUser('Anonymous')

        if "Authorization" not in request.headers:
            raise AuthenticationError('No basic auth credentials provided')

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        if config['username'] != username or config['password'] != password:
            raise AuthenticationError('Invalid username and password')
        return AuthCredentials(["authenticated"]), SimpleUser(username)

def on_auth_error(request, exc):
    return PlainTextResponse('Unauthorized', 401, headers={
        'WWW-Authenticate': 'Basic'
    })

app = Starlette(debug=True,
                routes=[
                    Route('/', homepage),
                    Route('/page/{page}', homepage),
                    Route('/main.css', css),
                    Mount('/static', app=StaticFiles(directory=resource_path('static')), name='static'),
                    WebSocketRoute('/ws', RemoteControl),
                ],
                middleware=[
                    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_auth_error)
                ])

def run_app():
    kwargs = {
    'host': config['bind_address'],
    'port': config['port'],
    }
    if config['ssl_enabled']:
        kwargs.update({
            'ssl_keyfile': config['ssl_keyfile'],
            'ssl_certfile': config['ssl_certfile']
        })
    try:
        uvicorn.run(app, **kwargs)
    except:
        logger.exception('web server error')

if __name__ == '__main__':
    run_app()