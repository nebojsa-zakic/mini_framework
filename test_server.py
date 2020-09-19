import mini_http.route.router as router
import mini_http.response as response
import mini_http.server as mini
import mini_http.route.interceptor as interceptor
import mini_http.route.path_rewriter as rewriter
import mini_http.static_server.file_cache as file_cache
import mini_http.log.logger as log
import mini_http.static_server.static as static

from datetime import date
import json as jsn
import threading
import tkinter as tk
import queue

# Port on which http server will be running
SERVER_PORT = 3333

# Commented in order to trigger db connection
# import app_repo as repo

# Class encodes dates so they can be serialized to JSON


class DateTimeEncoder(jsn.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return jsn.JSONEncoder.default(self, o)


# Echoes get path
def hello(req, path_vars):
    return response.ok(req['GET'], 'text/plain')

# Returns current date


def current_date(req):
    today = date.today().strftime("%d %B  %Y")
    return response.ok(today, 'text/plain')

# This works but it won't work on your machine since you don't have my database
# I've added image as proof
# def user_list(req):
#     users = repo.fetch_users()
#     stringified_users = jsn.dumps(users, cls=DateTimeEncoder)
#     return response.ok(stringified_users, 'application/json')

# Echoes recieved json


def json(req, body):
    string_json = body
    parsed_json = jsn.loads(string_json)

    return response.ok(jsn.dumps(parsed_json, separators=(',', ':')))

# Interceptor which allows all requests


def hello_world(param_map):
    log.info('Hello xD')
    return True

# Interceptor which blocks all requests


def nope_lolz(param_map):
    log.info('No')
    return False


def static_rewrite(path, ext):
    BASE_PATH = './static'
    INDEX_PAGE = '/index.html'

    file_path = BASE_PATH

    if path != '/':
        file_path += path
    else:
        file_path += INDEX_PAGE

    return file_path


def server_img(req, path_vars):
    if int(path_vars['num']) > 10 or int(path_vars['num']) <= 0:
        log.error("Image " + path_vars['num'] + " does not exist")
        return response.not_found("Image does not exist")

    return static.serve('./static/january/' + path_vars['num'] + '.jpg', skip_rewrite=True)


def html_rewrite(path, ext):
    if ext == '':
        return path + '.html'

    return path


def multi_param_text(req, path_vars):
    print(path_vars)
    return response.ok(path_vars['v1'] + ' ' + path_vars['v2'] + ' ' + path_vars['v3'], 'text/plain')


# This rewrites paths to hit /static folder before serving static file
rewriter.add_rewrite_logic(static_rewrite)
# This rewrites paths to include .html as an extension if they missing
rewriter.add_rewrite_logic(html_rewrite)

router.get('/abc/{v1}/def/{v2}/{v3}', multi_param_text)
router.get('/img/{num}', server_img)
router.get('/test/{abc}', hello)
router.post('/json', json)
router.get('/date', current_date)
# router.get('/users', user_list)

# I've had time only to implement interceptors which match with starts with

# Easy way to test interceptor
# interceptor.register('GET', '/', hello_world)

# This would throw 404 if it wasn't for the interceptor
interceptor.register('GET', '/json', nope_lolz)


def run_server():
    global SERVER_PORT
    display_messages = True
    log.info('Server is running on port ' + str(SERVER_PORT))
    log.info('Try accessing server at 127.0.0.1:' + str(SERVER_PORT) +
             '. It will serve items faster than localhost')
    log.set_log_level("trace")

    file_cache.precache("\\static", recursive=True)

    mini.server_port(SERVER_PORT)
    log.warn("This is a warning")
    log.error("This is an error")
    log.info("This is an info")
    log.debug("This is a debug message")
    log.trace("This is a trace message")
    print(router.get_routes)
    mini.start()


run_server()
