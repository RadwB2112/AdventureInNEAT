import os
import importlib
from PIL import Image

# because of circular import I need a separate file


def make_watchers(*modules, always_reload=()):
    watched = {mod: mod.__file__ for mod in modules}
    mtimes = {mod: os.path.getmtime(path) for mod, path in watched.items()}

    def watch_and_reload():
        for mod, path in watched.items():
            mtime = os.path.getmtime(path)
            if not os.path.exists(path):
                print(f"FNF {mod.__name__}: {path}")
                continue
            if mtime != mtimes[mod] or mod in always_reload:
                print(f"reloading {mod.__name__}")
                importlib.reload(mod)
                mtimes[mod] = mtime

    return watch_and_reload


def transform(x1, path):
    image = Image.open(f'images/{path}')
    width, height = image.size

    temp = width / x1

    return height / temp
