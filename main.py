import logging
import logging.handlers
import threading

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
log_handler = logging.handlers.RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=2)
log_handler.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('[%(asctime)s]    %(name)s    %(levelname)s   %(message)s')
log_handler.setFormatter(log_formatter)
root_logger.addHandler(log_handler)

import web
import gui

t = threading.Thread(target=web.run_app, daemon=True)
t.start()

gui.run_app()