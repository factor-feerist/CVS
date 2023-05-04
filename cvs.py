import sys
import os

class CVS:
    def __init__(self):
        def init(*args):
            if len(args) == 1:
                cwd = args[0]
            elif len(args) == 0:
                cwd = os.getcwd()
            else:
                raise ValueError
            path = os.path.join(cwd, '.cvs')
            os.mkdir(path)


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
    cvs.commands[cmd](*args)
except ValueError:
    cmd, *args = input().split()
    cvs.commands[cmd](*args)
