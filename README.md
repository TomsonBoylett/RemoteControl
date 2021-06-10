# Remote Control
Turns your phone into a remote control for your computer.

## What does this application do?
Allows you open a url on your phone which will display a grid of buttons. Clicking these button executes commands on your PC such as sending keystrokes and launching programs.

Each grid of buttons belongs to a page. Multiple pages can be created and linked together allowing you to switch between different layouts.

## Usage

### Installation and running the software

1. Extract the zip
2. Run the remote-control executable
3. A tray icon will appear. Right clicking this allows you to exit the program. Left clicking opens the remote control in your default browser. Alternatively, you can visit http://127.0.0.1:8000 in your browser.
4. Output is logged to the app.log file in the same location as the executable.
5. See the configuration section below to allow access to the remote control from another device.

When accessing the remote control from a mobile phone it is recommended to use Chrome and add the link to the homescreen. This causes the page to be displayed in fullscreen without a url bar. This application does not work in Safari or Internet Explorer.

### Configuration
Edit the config.toml to setup the button layout to your liking. The config.toml provided will work out of the box and provides examples of how to define each page and its buttons.

You need to change the bind_address from 127.0.0.1 to 0.0.0.0 to allow access from another device.

The application must be restarted to reflect changes to the config.

## Running from source
Python 3.8+ required
```
pip install -r requirements.txt
python main.py
```

The application has only been tested in Windows 10 but it may be able to run on other platforms.

## Credits
Remote control icon by Vectors Market https://thenounproject.com/vectorsmarket/
