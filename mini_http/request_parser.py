HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'CONNECT']

def form_query_params(query_params_string):
    params = dict()
    # Array of key=value
    query_params_pairs = query_params_string[0].split('&')

    for pair in query_params_pairs:
        key = pair.split("=")[0]
        value = pair.split("=")[1]
        params[key] = value

    return params


def parse(req):
    decoded_req = req.decode()

    req_param_map = dict()

    body = None
    method = None

    if '\r\n\r\n' in decoded_req:
        body = decoded_req.split('\r\n\r\n')[1]

    for line in decoded_req.split('\n'):
        if line == '\r':
            break

        param = line.split(' ')[0]

        if param and len(param) > 0 and param[-1] == ':':
            param = param[:-1]

        value = ' '.join(line.split(' ')[1:])

        if param in HTTP_METHODS:
            method = param
            value = value.split(' ')[0]

            if '?' in value:
                query_params = value.split('?')[1:]
                req_param_map['query_params'] = form_query_params(query_params)
                value = value.split('?')[0]

        if '\r' in value:
            value = value.replace('\r', '')

        req_param_map[param] = value

    return req_param_map, body, method
