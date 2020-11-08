from datetime import datetime as dt

WARN_COLOR = '\033[93m'
ERROR_COLOR = '\033[91m'
TRACE_COLOR = '\033[90m'
DEBUG_COLOR = '\033[95m'
END_COLOR = '\033[0m'


# Log levels:
# 0 - Error
# 1 - Warning
# 2 - Info
# 3 - Debug
# 4 - Trace

LOG_LEVEL = 2

def is_debugging():
    return LOG_LEVEL >= 3

def is_tracing():
    return LOG_LEVEL >= 3

def set_log_level(log_level):
    global LOG_LEVEL

    if isinstance(log_level, int):
        if log_level >= 0 and log_level <= 4:
            LOG_LEVEL = log_level
            if is_debugging():
                debug("Logger level set to level: " + str(LOG_LEVEL))
        else:
            raise Exception("Invalid log level: " + str(log_level))
    else:
        if log_level.lower() == "error".lower():
            LOG_LEVEL = 0
        if log_level.lower() == "warning".lower():
            LOG_LEVEL = 1
        if log_level.lower() == "info".lower():
            LOG_LEVEL = 2
        if log_level.lower() == "debug".lower():
            LOG_LEVEL = 3
        if log_level.lower() == "trace".lower():
            LOG_LEVEL = 4
        if is_debugging():
            debug("Logger level set to level: " + log_level.lower())



def _get_now():
    return str(dt.now().time())[:8]


def _handle_print(date_text, level, message, text_color=None):
    if text_color == None:
        print(date_text + " " + level + ": " + str(message))
    else:
        print(text_color + date_text + " " +
              level + ": " + str(message) + END_COLOR)


def error(message, show_date=True):
    global LOG_LEVEL

    if LOG_LEVEL < 0:
        return

    if show_date:
        _handle_print(_get_now(), "Error", message, ERROR_COLOR)
    else:
        _handle_print("", "Error", message, ERROR_COLOR)


def warn(message, show_date=True):
    global LOG_LEVEL

    if LOG_LEVEL < 1:
        return

    if show_date:
        _handle_print(_get_now(), "Warning", message, WARN_COLOR)
    else:
        _handle_print("", "Warning", message, WARN_COLOR)


def info(message, show_date=True):
    global LOG_LEVEL

    if LOG_LEVEL < 2:
        return

    if show_date:
        _handle_print(_get_now(), "Info", message)
    else:
        _handle_print("", "Info", message)


def debug(message, show_date=True):
    global LOG_LEVEL

    if LOG_LEVEL < 3:
        return

    if show_date:
        _handle_print(_get_now(), "Debug", message, DEBUG_COLOR)
    else:
        _handle_print("", "Debug", message, DEBUG_COLOR)


def trace(message, show_date=True):
    global LOG_LEVEL

    if LOG_LEVEL < 4:
        return

    if show_date:
        _handle_print(_get_now(), "Trace", message, TRACE_COLOR)
    else:
        _handle_print("", "Trace", message, TRACE_COLOR)
