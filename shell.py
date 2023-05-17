import cmd
import os
import sys
from modules.cvs import CVS

class CVSShell(cmd.Cmd):
    intro = 'Welcome to the CVS shell'
    prompt = None
    def __init__(self):
        super().__init__()
        self._current_directory = os.getcwd()
        CVSShell.prompt = f'{self._current_directory}>'

    def do_cd(self, directory):
        '''Changes current directory'''
        try:
            if ':' in directory:
                self._current_directory = directory
            else:
                self._current_directory = os.path.join(self._current_directory, directory)
            CVSShell.prompt = f'{self._current_directory}>'
            os.chdir(self._current_directory)
        except OSError:
            print(f'Can\'t find directory \"{directory}\"')

    def do_mkdir(self, directory):
        '''Creates a new directory'''
        try:
            os.mkdir(os.path.join(self._current_directory, directory))
        except FileExistsError:
            print(f'Directory {directory} already exists')

    def do_touch(self, filename):
        '''Creates a new file'''
        try:
            with open(filename) as f:
                print(f'File {filename} already exists')
        except OSError:
            with open(filename, 'w') as f:
                pass

    def do_ls(self, arg):
        '''Shows all files in current directory'''
        for item in os.listdir(self._current_directory):
            print(item)

    def do_init(self, arg):
        '''Initialize repository in current directory'''
        self.cvs = CVS(self._current_directory)

    def precmd(self, line):
        print()
        return line

if __name__ == '__main__':
    CVSShell().cmdloop()
