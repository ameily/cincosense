import threading

from kivy.clock import Clock
from kivy.logger import Logger


MAIN_TID = threading.get_ident()

def only_main_thread(func):
    def wrapper(*args, **kwargs):
        if threading.get_ident() != MAIN_TID:
            Clock.schedule_once(lambda dt: func(*args, **kwargs))
            return
        func(*args, **kwargs)
    return wrapper


def wakeup_tty(filename: str) -> None:
    print('HERE')
    try:
        with open(filename, 'wb') as fp:
            fp.write(b'\x1b[13]')
    except:
        Logger.exception('wakeup_tty: failed to wake up tty: %s', filename)
    else:
        Logger.info('wakeup_tty: woke up tty: %s', filename)
