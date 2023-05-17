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
        self.cvs = None
        CVSShell.prompt = f'{self._current_directory}>'

    def do_cd(self, directory):
        '''Changes current directory'''
        try:
            if ':' in directory:
                os.chdir(directory)
                self._current_directory = directory
            else:
                os.chdir(os.path.join(self._current_directory, directory))
                self._current_directory = os.path.join(self._current_directory, directory)
            CVSShell.prompt = f'{self._current_directory}>'
        except OSError:
            print(f'*** Can\'t find directory \"{directory}\"')

    def do_mkdir(self, directory):
        '''Creates a new directory'''
        try:
            os.mkdir(os.path.join(self._current_directory, directory))
        except FileExistsError:
            print(f'*** Directory {directory} already exists')

    def do_touch(self, filename):
        '''Creates a new file'''
        try:
            with open(filename) as f:
                print(f'*** File {filename} already exists')
        except OSError:
            with open(filename, 'w') as f:
                pass

    def do_ls(self, arg):
        '''Shows all files in current directory'''
        for item in os.listdir(self._current_directory):
            print(f'    {item}')

    def do_init(self, arg):
        '''Initializes repository in current directory'''
        if CVS.is_initialized(self._current_directory):
            print(f'*** Directory {self._current_directory} is already a repository')
        else:
            self.cvs = CVS(self._current_directory)
            self.cvs.init()

    def do_add(self, arg):
        '''Adds mentioned files in current directory to stage'''
        if self.cvs == None:
            if CVS.is_initialized(self._current_directory):
                self.cvs = CVS(self._current_directory)
            else:
                print('*** No repository in this directory')
                return
        if arg == '.':
            for path in os.listdir('.'):
                self.do_add(os.path.join(self._current_directory, path))
        else:
            for item in arg.split():
                if ':' in item:
                    path = item
                else:
                    path = f'{self._current_directory}\\{item}'
                if os.path.isdir(path):
                    if path == f'{self._current_directory}\\.cvs':
                        return
                    for e in os.listdir(path):
                        self.do_add(os.path.join(path, e))
                elif os.path.isfile(path):
                    self.cvs.add_file(path)
                else:
                    print(f'*** No such directory or file: {path}')

    def do_log(self, arg):
        '''Prints stage log'''
        if self.cvs == None:
            if CVS.is_initialized(self._current_directory):
                self.cvs = CVS(self._current_directory)
            else:
                print('*** No repository in this directory')
                return
        self.cvs.log()

    def precmd(self, line):
        print()
        return line

if __name__ == '__main__':
    CVSShell().cmdloop()
