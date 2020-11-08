OK = "200 OK"
CREATED = "201 CREATED"
ACCEPTED = "204 ACCEPTED"
NOT_FOUND = "404 NOT FOUND"
FORBIDDEN = "403 FORBIDDEN"
BAD_REQUEST = "400 BAD_REQUEST"

HTTP_VERSION = 'HTTP/1.1'


def enc_bytes(string):
    return bytes(string.encode())


def build(status, responseType, body, headers={}):
    global HTTP_VERSION
    response = HTTP_VERSION + " " + status + "\n"
    response += "Content-Type: " + responseType + "\n"

    for header_data in headers.items():
        response += header_data[0] + ": " + header_data[1] + "\n"

    response += "\n"

    response += body + "\n"
    return enc_bytes(response)


def build_from_bytes(status, body, headers={}):
    global HTTP_VERSION
    response = HTTP_VERSION + " " + status + "\n"

    for header_data in headers.items():
        response += header_data[0] + ": " + header_data[1] + "\n"

    response += "\n"

    return enc_bytes(response) + body + enc_bytes('\n')


def ok(body, responseType="text/html", headers={}):
    return build(OK, responseType, body, headers)


def not_found(message, responseType="text/plain", headers={}):
    return build(NOT_FOUND, responseType, message, headers)


def forbidden(message, responseType="text/plain", headers={}):
    return build(FORBIDDEN, responseType, message, headers)

def bad_request(message, responseType="text/plain", headers={}):
    return build(BAD_REQUEST, responseType, message, headers)
