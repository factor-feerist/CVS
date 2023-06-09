import cmd
import os
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
        'Changes current directory\n> cd directory'
        try:
            if ':' in directory:
                os.chdir(directory)
                self._current_directory = directory
            else:
                os.chdir(os.path.join(self._current_directory, directory))
                self._current_directory = os.path.join(self._current_directory,
                                                       directory)
            CVSShell.prompt = f'{self._current_directory}>'
        except OSError:
            print(f'*** Can\'t find directory \"{directory}\"')

    def do_mkdir(self, directory):
        'Creates a new directory\n> mkdir directory'
        try:
            os.mkdir(os.path.join(self._current_directory, directory))
        except FileExistsError:
            print(f'*** Directory {directory} already exists')

    def do_touch(self, filename):
        'Creates a new file\n> touch file'
        try:
            with open(filename):
                print(f'*** File {filename} already exists')
        except OSError:
            with open(filename, 'w'):
                pass

    def do_ls(self, arg):
        'Shows all files in current directory\n> ls'
        for item in os.listdir(self._current_directory):
            print(f'    {item}')

    def do_init(self, arg):
        'Initializes repository in current directory\n> init'
        if CVS.is_initialized(self._current_directory):
            print(f'*** Directory {self._current_directory} is already a '
                  f'repository')
        else:
            self.cvs = CVS(self._current_directory)
            self.cvs.init()
            print('Repository initialized')

    def do_add(self, arg):
        'Adds mentioned files or directories in current directory to stage:' \
            '\n> add file1 file2 ... dir1 dir2 ...' \
            '\nAdds all files in current directory to stage:' \
            '\n> add .'
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
                    print(f'Added to stage {item}')
                else:
                    print(f'*** No such directory or file: {path}')

    def do_slog(self, arg):
        'Prints stage log\n> slog'
        if not self.is_repository():
            return
        print(self.cvs.stage_log())

    def do_commit(self, message):
        'Makes a commit with mentioned message\n> commit message'
        if not self.is_repository():
            return
        h = self.cvs.commit(message)
        print(f'*** Changes were committed successfully: commit {h}')

    def do_clog(self, arg):
        'Prints commit log\n> clog'
        if not self.is_repository():
            return
        print(self.cvs.commit_log())

    def do_branch(self, arg):
        'Creates branch with mentioned name:' \
            '\n> branch name' \
            '\nRemoves branch with mentioned name:' \
            '\n> branch name r'
        if not self.is_repository():
            return
        ops = arg.split()
        name = ops[0]
        if len(ops) == 2 and ops[1] == 'r':
            try:
                self.cvs.remove_branch(name)
                print(f'*** Removed branch {name}')
            except Exception as e:
                print(e)
        elif len(ops) == 1:
            try:
                self.cvs.create_branch(name)
                print(f'*** Created branch {name}')
            except Exception as e:
                print(e)

    def do_tag(self, arg):
        'Creates tag with mentioned name and message:' \
            '\n> tag name message' \
            '\nRemoves tag with mentioned name:' \
            '\n> tag name r'
        if not self.is_repository():
            return
        ops = arg.split()
        name = ops[0]
        if len(ops) == 2 and ops[1] == 'r':
            try:
                self.cvs.remove_tag(name)
                print(f'*** Removed tag {name}')
            except Exception as e:
                print(e)
        elif len(ops) >= 2:
            try:
                message = ' '.join(ops[1::])
                self.cvs.create_tag(name, message)
                print(f'*** Created tag {name} with message: {message}')
            except Exception as e:
                print(e)
        else:
            print('Incorrect format')

    def do_tlog(self, arg):
        'Prints tag log\n> tlog'
        if not self.is_repository():
            return
        print(self.cvs.tag_log())

    def do_checkout(self, arg):
        'Switch version of repository by commit/branch/tag' \
            '\n> checkout commit/branch/tag'
        if not self.is_repository():
            return
        try:
            self.cvs.checkout(arg)
            print('Repository version changed successfully')
        except Exception as e:
            print(e)

    def precmd(self, line):
        print()
        return line

    def is_repository(self):
        if self.cvs is None:
            if CVS.is_initialized(self._current_directory):
                self.cvs = CVS(self._current_directory)
            else:
                print('*** No repository in this directory')
                return False
        return True


if __name__ == '__main__':
    CVSShell().cmdloop()
