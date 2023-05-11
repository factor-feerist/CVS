import sys
import os

class CVS:
    def __init__(self):
        def init(path = None):
            if path is not None:
                cwd = path
            else:
                cwd = os.getcwd()
            path = os.path.join(cwd, '.cvs')
            os.mkdir(path)
            file_path = os.path.join(path, 'index')
            with open(file_path, 'w'):
                pass
            

        def add(*args):
            pass


        def commit(*args):
            pass


        def reset(*args):
            pass


        def log(*args):
            pass

        self.commands = {
                    'init': init,
                    'add': add,
                    'commit': commit,
                    'ci': commit,
                    'reset': reset,
                    'log': log
                    }
   

cvs = CVS()
try:
    cmd, *args = sys.argv[1:]
except ValueError:
    cmd, *args = input().split()
cvs.commands[cmd](*args)
