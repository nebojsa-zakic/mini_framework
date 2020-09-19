import mini_http.request_parser as request_parser
import mini_http.route.router as router
import mini_http.response as response
import mini_http.route.interceptor as interceptor
import mini_http.static_server.static as static
import mini_http.log.logger as log

MAX_REQUEST_SIZE = 10 * 1024


def handle_conn(conn):
    global MAX_REQUEST_SIZE
    req = conn.recv(MAX_REQUEST_SIZE)
    req_param_map, body, method = request_parser.parse(req)

    if method not in req_param_map:
        conn.close()
        log.warn("Method not found. Closing connection.")
        return

    interception_passed = interceptor.execute(
        method, req_param_map[method], req_param_map, body)

    if not interception_passed:
        if log.is_tracing():
            log.trace("Request intercepted connection not allowed: " +
                      req_param_map[method])
        conn.send(response.forbidden(""))
        conn.close()
        return

    try:
        res = router.resolve(req_param_map, body)
        if res == None and method == 'GET':
            res = static.serve(req_param_map[method])

        if res == None and method == 'HEAD':
            res = static.file_exists(req_param_map[method])

        if res == None:
            raise Exception("Path not found: " + req_param_map[method])

        conn.send(res)
    except Exception as e:
        log.debug(e)
        conn.send(response.not_found(""))

    conn.close()
