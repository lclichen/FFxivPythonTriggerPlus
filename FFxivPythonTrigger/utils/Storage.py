import sys
import pathlib
import json


class Storage(object):
    def __init__(self):
        self.base_path = pathlib.Path(sys.argv[0]).parents[0] / 'AppData'
        self.base_path.mkdir(exist_ok=True, parents=True)

    def get_plugin_storage(self, name: str):
        return ModuleStorage(self.base_path / 'Plugins' / name.replace(' ','_'))

    def get_core_storage(self):
        return ModuleStorage(self.base_path / "Core")


class ModuleStorage(object):
    def __init__(self, path: pathlib.Path):
        self._path = path
        if self._path.exists():
            self.load()
        else:
            self.data = dict()
    @property
    def path(self):
        self._path.mkdir(exist_ok=True, parents=True)
        return self._path

    def load_new(self):
        self.data = dict()

    def load(self):
        file = self._path / 'data'
        try:
            size = file.stat().st_size
        except:
            self.load_new()
        else:
            if not size:
                self.load_new()
            else:
                with open(file) as fi:
                    try:
                        self.data = json.load(fi)
                    except json.decoder.JSONDecodeError:
                        self.data = fi.read()

    def store(self):
        if self.data:
            self._path.mkdir(exist_ok=True, parents=True)
            with open(self._path / 'data', 'w+') as fo:
                fo.write(json.dumps(self.data, indent=4))
