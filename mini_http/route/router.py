get_routes = []
post_routes = []
put_routes = []
delete_routes = []
patch_routes = []
options_routes = []
head_routes = []
connect_routes = []
trace_routes = []


def resolve(req_param_map, body):
    if 'GET' in req_param_map:
        get_route_data = find_get(req_param_map['GET'])
        # callback is null when static content is requested
        if get_route_data == None:
            return None

        return get_route_data['callback'](req_param_map, get_route_data['path_variables'])
    elif 'POST' in req_param_map:
        post_route_data = find_post(req_param_map['POST'])
        if post_route_data == None:
            return None
        return post_route_data['callback'](req_param_map, body, post_route_data['path_variables'])
    elif 'PUT' in req_param_map:
        put_route_data = find_put(req_param_map['PUT'])
        if put_route_data == None:
            return None
        return put_route_data['callback'](req_param_map, body, put_route_data['path_variables'])
    elif 'DELETE' in req_param_map:
        delete_route_data = find_delete(req_param_map['DELETE'])
        if delete_route_data == None:
            return None
        return delete_route_data['callback'](req_param_map, body, delete_route_data['path_variables'])
    elif 'PATCH' in req_param_map:
        patch_route_data = find_patch(req_param_map['PATCH'])
        if patch_route_data == None:
            return None
        return patch_route_data['callback'](req_param_map, body, patch_route_data['path_variables'])
    elif 'OPTIONS' in req_param_map:
        options_route_data = find_options(req_param_map['OPTIONS'])
        if options_route_data == None:
            return None
        return options_route_data['callback'](req_param_map, options_route_data['path_variables'])
    elif 'HEAD' in req_param_map:
        head_route_data = find_head(req_param_map['HEAD'])
        if head_route_data == None:
            return None
        return head_route_data['callback'](req_param_map, head_route_data['path_variables'])
    elif 'TRACE' in req_param_map:
        trace_route_data = find_trace(req_param_map['TRACE'])
        if trace_route_data == None:
            return None
        return trace_route_data['callback'](req_param_map, trace_route_data['path_variables'])
    elif 'CONNECT' in req_param_map:
        connect_route_data = find_trace(req_param_map['CONNECT'])
        if connect_route_data == None:
            return None
        return connect_route_data['callback'](req_param_map, connect_route_data['path_variables'])
    else:
        raise Exception("Unknown method")

# Registration functions


def _compare_routes(reg_route, recv_route):
    # this part can be optimized both speed can go to O(n)
    # memory to O(K)
    reg_elements = reg_route.split('/')
    recv_elements = recv_route.split('/')

    if len(reg_elements) != len(recv_elements):
        return False

    for reg_e, recv_e in zip(reg_elements, recv_elements):
        if reg_e == '_' or reg_e == recv_e:
            continue
        return False

    return True


# extracts data from a route
# returns a map with parsed data
def _parse_variable_values(route, variable_data):
    variables = dict()

    i = 0
    # corrects starting index of path variable since there can be multiple
    # length of previous variable is added to real index position
    curr_var_length = 0

    # variable data is always sorted by variable index asceding
    for var_datum in variable_data:
        var_name = var_datum['var_name']
        index = var_datum['index']

        var_value = ''

        for c in route[(index + curr_var_length):]:
            # to be replaced with a variable character
            if c == '/':
                break

            var_value += c
            curr_var_length += 1

        variables[var_name] = var_value

        i += 1

    return variables


def _parse_path_variables(route):
    if '{' not in route or '}' not in route:
        return route, {}

    parsed_route = ''

    parsing_var = False
    variables = []
    current_var = ''
    current_var_index = -1

    last_var_name_length = 0

    i = 0

    for c in route:
        if c == '{':
            if parsing_var:
                raise Exception("Invalid route: " + route)
            parsing_var = True
            current_var = ''
            current_var_index = i - last_var_name_length
            parsed_route += '_'
            # +2 at start describes places for { and }
            last_var_name_length += 2
            i += 1
            continue

        if c == '}':
            if not parsing_var:
                raise Exception("Invalid route: " + route)
            parsing_var = False
            variables.append(
                {"var_name": current_var, "index": current_var_index})
            i += 1
            continue

        if c == '/' and parsing_var:
            raise Exception("Invalid route: " + route)

        if parsing_var:
            current_var += c
            last_var_name_length += 1
        else:
            parsed_route += c

        i += 1

    return parsed_route, variables


def _append_to_routes_list_data(route_list, route, callback):
    parsed_route, variables = _parse_path_variables(route)
    route_list.append({"parsed_route": parsed_route,
                       "variables": variables, "callback": callback})


def get(route, callback):
    global get_routes, head_routes
    _append_to_routes_list_data(get_routes, route, callback)
    _append_to_routes_list_data(head_routes, route, callback)


def post(route, callback):
    global post_routes
    _append_to_routes_list_data(post_routes, route, callback)


def put(route, callback):
    global put_routes
    _append_to_routes_list_data(put_routes, route, callback)


def delete(route, callback):
    global delete_routes
    _append_to_routes_list_data(delete_routes, route, callback)


def patch(route, callback):
    global patch_routes
    _append_to_routes_list_data(patch_routes, route, callback)


def options(route, callback):
    global options_routes
    _append_to_routes_list_data(options_routes, route, callback)


def trace(route, callback):
    global trace_routes
    _append_to_routes_list_data(trace_routes, route, callback)


def connect(route, callback):
    global connect_routes
    _append_to_routes_list_data(connect_routes, route, callback)


def head(route, callback):
    global head_routes
    _append_to_routes_list_data(head_routes, route, callback)


# Search functions


def _find_from_routes(route_data_list, route):
    for route_data in route_data_list:
        if _compare_routes(route_data['parsed_route'], route):
            return {
                "callback": route_data['callback'],
                "path_variables": _parse_variable_values(route, route_data['variables'])
            }

    return None


def find_get(route):
    global get_routes
    return _find_from_routes(get_routes, route)


def find_post(route):
    global post_routes
    return _find_from_routes(post_routes, route)


def find_put(route):
    global put_routes
    return _find_from_routes(put_routes, route)


def find_delete(route):
    global delete_routes
    return _find_from_routes(delete_routes, route)


def find_patch(route):
    global patch_routes
    return _find_from_routes(patch_routes, route)


def find_options(route):
    global options_routes
    return _find_from_routes(options_routes, route)


def find_trace(route):
    global trace_routes
    return _find_from_routes(trace_routes, route)


def find_head(route):
    global head_routes
    return _find_from_routes(head_routes, route)


def find_connect(route):
    global connect_routes
    return _find_from_routes(connect_routes, route)
