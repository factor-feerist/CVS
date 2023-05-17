import sys
import os

class CVS:
    def __init__(self, directory):
        self.directory = directory
        os.mkdir(f'{directory}\\.cvs')
        os.mkdir(f'{directory}\\.cvs\\objects')
        with open(f'{directory}\\.cvs\\index', 'w'):
            pass

    @staticmethod
    def is_initialized(directory):
        return os.path.isdir(f'{directory}/.cvs')
