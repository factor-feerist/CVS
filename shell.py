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
        if not self.is_repository():
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

    def do_slog(self, arg):
        '''Prints stage log'''
        if not self.is_repository():
            return
        print(self.cvs.stage_log())

    def do_commit(self, message):
        '''Makes a commit with mentioned message'''
        if not self.is_repository():
            return
        self.cvs.commit(message)
        print(f'*** Changes were commited succesfully: commit {h}')

    def do_clog(self, arg):
        '''Prints commit log'''
        if not self.is_repository():
            return
        print(self.cvs.commit_log())

    def do_branch(self, arg):
        '''Creates branch with mentioned name: branch name\nRemoves branch with mentioned name: branch name r'''
        if not self.is_repository():
            return
        ops = arg.split()
        name = ops[0]
        if len(ops) == 2 and ops[1] == 'r':
            self.cvs.remove_branch(name)
            print(f'*** Removed branch {name}')
        elif len(ops) == 1:
            self.cvs.create_branch(name)
            print(f'*** Created branch {name}')
        
    def precmd(self, line):
        print()
        return line

    def is_repository(self):
        if self.cvs == None:
            if CVS.is_initialized(self._current_directory):
                self.cvs = CVS(self._current_directory)
            else:
                print('*** No repository in this directory')
                return False
        return True


if __name__ == '__main__':
    CVSShell().cmdloop()
