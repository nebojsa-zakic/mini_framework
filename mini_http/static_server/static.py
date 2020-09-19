import mini_http.response as response
import mini_http.route.path_rewriter as rewriter
import mini_http.static_server.file_cache as file_cache
import mini_http.log.logger as log

def file_exists(path, skip_rewrite=False, ignore_cache=False):
    if not skip_rewrite:
        rewritten_fp = rewriter.rewrite(path)
    else:
        rewritten_fp = path

    if log.is_tracing():
        log.trace("Accessing path: " + rewritten_fp)

    if not ignore_cache:
        cached_file = file_cache.get_file(rewritten_fp)
        if cached_file != None:
            response.ok("")

    file = open(rewritten_fp, 'rb')

    if file == None:
        return response.not_found("")

    return response.ok("")

def serve(path, skip_rewrite=False, ignore_cache=False):

    if not skip_rewrite:
        rewritten_fp = rewriter.rewrite(path)
    else:
        rewritten_fp = path

    if log.is_tracing():
        log.trace("Accessing path: " + rewritten_fp)

    if not ignore_cache:
        cached_file = file_cache.get_file(rewritten_fp)
        if cached_file != None:
            return response.build_from_bytes('200 OK', cached_file)

    file = open(rewritten_fp, 'rb')

    if file == None:
        return None

    return response.build_from_bytes('200 OK', file.read())
