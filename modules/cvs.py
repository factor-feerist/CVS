import sys
import os
from datetime import datetime
from modules.utilities import get_hash, Blob


class CVS:
    def __init__(self, directory):
        self.directory = directory
        
    def init(self):
        os.mkdir(f'{self.directory}\\.cvs')
        os.mkdir(f'{self.directory}\\.cvs\\objects')
        with open(f'{self.directory}\\.cvs\\index', 'w'):
            pass
        with open(f'{self.directory}\\.cvs\\log', 'w'):
            pass

    @staticmethod
    def is_initialized(directory):
        return os.path.isdir(f'{directory}/.cvs')

    def add_file(self, path):
        with open(path) as f:
            content = f.read()
        h = get_hash(content)
        blob_path = f'{self.directory}\\.cvs\\objects\\{h[:2]}'
        if not os.path.exists(blob_path):
            os.mkdir(blob_path)
        with open(f'{blob_path}\\{h[2:]}', 'wb') as f:
            f.write(Blob(content).serialize())

        if os.path.exists(f'{self.directory}\\.cvs\\index'):
            with open(f'{self.directory}\\.cvs\\index') as f:
                index = f.read()
        else:
            index = ''
        d = {}
        for line in index.split('\n'):
            ops = line.split('\\\\')
            if len(ops) == 2:
                d[ops[0]] = ops[1]
        
        if path in d.keys() and not h == d[path]:
            with open(f'{self.directory}\\.cvs\\log', 'a') as f:
                f.write(f'{datetime.now().strftime("%d/%m/%y %H:%M:%S")}\\\\CHANGED\\\\{path}\\\\{d[path]}\\\\{h}\n')
                d[path] = h
        elif path not in d.keys():
            d[path] = h
            with open(f'{self.directory}\\.cvs\\log', 'a') as f:
                f.write(f'{datetime.now().strftime("%d/%m/%y %H:%M:%S")}\\\\ADDED\\\\{path}\\\\{d[path]}\n')

        with open(f'{self.directory}\\.cvs\\index', 'w') as f:
            for key, value in d.items():
                f.write(f'{key}\\\\{value}\n')
        