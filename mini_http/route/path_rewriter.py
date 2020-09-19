import mini_http.log.logger as log

rewrite_callbacks = list()

def add_rewrite_logic(callback):
    global rewrite_callbacks
    rewrite_callbacks.append(callback)

def extension(path):
    if '/' not in path:
        return ''

    last_elem = path.split('/')[-1]

    if '.' not in last_elem:
        return ''

    return last_elem.split('.')[-1]


def rewrite(file_path):
    global rewrite_callbacks

    rewritten_file_path = file_path

    for rewrite_callback in rewrite_callbacks:
        ext = extension(rewritten_file_path)

        rewritten_file_path = rewrite_callback(rewritten_file_path, ext)

    return rewritten_file_path