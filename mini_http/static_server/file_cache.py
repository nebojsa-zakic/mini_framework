import os
import glob
import mini_http.log.logger as log

_file_cache = dict()
_root_dir = os.getcwd()

# Root dir must be set prior to precaching folder outside of main file
def set_root_dir(dir):
    _root_dir = dir

def get_file(file_destination):
    if file_destination in _file_cache:
        return _file_cache[file_destination]
    if log.is_debugging():
        log.debug("File " + file_destination + " has not been found within cache.")
    return None


def cache_file(file_destination):
    if os.path.isdir(file_destination):
        raise Exception("Destination is not a path: " + file_destination)
    file = open(file_destination, 'rb')
    cached_file_name = "." + file_destination[len(_root_dir):].replace("\\", "/")
    if log.is_debugging():
        log.debug("Caching file: " + cached_file_name)
    _file_cache[cached_file_name] = file.read()


def precache(destination, recursive=False):
    global _root_dir
    prep_dest = destination
    if destination.startswith(_root_dir) == False:
        prep_dest = _root_dir + prep_dest

    if os.path.isdir(prep_dest):
        if log.is_tracing():
            log.trace("Caching folder content: " + prep_dest)
        for file_dest in glob.glob(prep_dest + "/*"):
            if os.path.isfile(file_dest):
                cache_file(file_dest)
            elif os.path.isdir(file_dest) and recursive == True:
                precache(file_dest, recursive=True)
    else:
        cache_file(prep_dest)
