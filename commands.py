import subprocess
import re
import logging

import pyautogui
pyautogui.FAILSAFE = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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

COMMANDS = {
    'keyboard': press_hotkey,
    'hotkey': press_hotkey,
    'launch': launch_program
}