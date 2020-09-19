_interceptors = list()

METHODS_WITH_BODY = ['POST', 'PUT', 'DELETE']


def register(method, path, callback):
    _interceptors.append((method, path, callback,))


def execute(method, path, request_params, body):
    for int_method, int_path, callback in _interceptors:

        if method != int_method:
            continue

        if path[0] == '/' and not path in int_path or not path.startswith(int_path):
            continue

        if method in METHODS_WITH_BODY:
            if not callback(request_params, body):
                return False
        else:
            if not callback(request_params):
                return False

    return True
