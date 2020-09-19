OK = "200 OK"
NOT_FOUND = "404 NOT FOUND"
FORBIDDEN = "403 FORBIDDEN"

def enc_bytes(string):
    return bytes(string.encode())


def build(status, responseType, body):
    response = "HTTP/1.1 " + status + "\n"
    response += "Content-Type: " + responseType + "\n" + "\n"
    response += body + "\n"
    return enc_bytes(response)

def build_from_bytes(status, body):
    response = "HTTP/1.1 " + status + "\n"
    response += "\n"

    return enc_bytes(response) + body + enc_bytes('\n')

def ok(body, responseType = "text/html"):
    return build(OK, responseType, body)

def not_found(message):
    return build(NOT_FOUND, "text/plain", message)

def forbidden(message):
    return build(FORBIDDEN, "text/plain", message)