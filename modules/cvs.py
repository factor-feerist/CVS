import sys
import os
from datetime import datetime
from modules.utilities import get_hash, read_index
from modules.objects import Blob, Tree


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
        blob = Blob(self.directory, path)
        h = blob.hash
        d = read_index(self.directory)
        
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
        
    def log(self):
        with open(f'{self.directory}\\.cvs\\log') as f:
            content = f.read()
        print(content)

    def commit(self, message):
        pass
    