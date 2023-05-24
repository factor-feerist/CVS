import sys
import os
from datetime import datetime
from modules.utilities import get_hash, read_index
from modules.objects import Blob, Tree
from modules.branch_handler import BranchHandler


class CVS:
    def __init__(self, directory):
        self.directory = directory
        self.branch_handler = BranchHandler(directory)
        
    def init(self):
        os.mkdir(f'{self.directory}\\.cvs')
        os.mkdir(f'{self.directory}\\.cvs\\objects')
        os.mkdir(self._path + '\\.cvs\\refs')
        os.mkdir(self._path + '\\.cvs\\refs\\heads')
        with open(self._path + '\\.cvs\\HEAD', 'w') as f:
            f.write('ref:refs/heads/master')
        with open(f'{self.directory}\\.cvs\\index', 'w'):
            pass
        with open(f'{self.directory}\\.cvs\\stagelog', 'w'):
            pass
        with open(f'{self.directory}\\.cvs\\commitlog', 'w'):
            pass
        

    @staticmethod
    def is_initialized(directory):
        return os.path.isdir(f'{directory}/.cvs')

    def add_file(self, path):
        with open(path) as f:
            content = f.read()
        h = Blob(self.directory, content).hash
        
        d = read_index(self.directory)
        
        if path in d.keys() and h != d[path]:
            with open(f'{self.directory}\\.cvs\\stagelog', 'a') as f:
                f.write(f'{datetime.now().strftime("%d/%m/%y %H:%M:%S")}\\\\CHANGED\\\\{path}\\\\{d[path]}\\\\{h}\n')
                d[path] = h
        elif path not in d.keys():
            d[path] = h
            with open(f'{self.directory}\\.cvs\\stagelog', 'a') as f:
                f.write(f'{datetime.now().strftime("%d/%m/%y %H:%M:%S")}\\\\ADDED\\\\{path}\\\\{d[path]}\n')

        with open(f'{self.directory}\\.cvs\\index', 'w') as f:
            for key, value in d.items():
                f.write(f'{key}\\\\{value}\n')
        
    def stage_log(self):
        with open(f'{self.directory}\\.cvs\\stagelog') as f:
            return f.read()

    def commit(self, message):
        tree = Tree(self.directory)
        removed = tree.not_processed
        branch = self.branch_handler.get_head_branch()
        if branch is None:
            parent = self.branch_handler.get_head_commit()
        else:
            parent = self.branch_handler.get_commit_by_branch(branch)
        commit = f'tree {tree.hash}\nparent {parent}\n\n{message}'
        h = Blob(commit).hash

        with open(f'{self.directory}\\.cvs\\commitlog') as f:
            clog = f.read()
        with open(f'{self.directory}\\.cvs\\commitlog', 'a') as f:
            f.write(f'Commit\\\\{h}\\\\{datetime.now().strftime("%d/%m/%y %H:%M:%S")}\\\\{message}\n')
            if parent is not None:
                prev_log = clog[clog.index(parent)::]
            for item in removed:
                f.write(f'  - {item} removed')
            d = read_index()
            for item in d.keys():
                if parent is None:
                    f.write(f'  - {item} added')
                elif d[item] not in prev_log:
                    if item in prev_log:
                        f.write(f'  - {item} changed')
                    else:
                        f.write(f'  - {item} added')
        if branch is None:
            self.branch_handler.set_head_to_commit(h)
        self.branch_handler.set_commit_by_branch(branch, h)

    def commit_log(self):
        with open(f'{self.directory}\\.cvs\\commitlog') as f:
            return f.read()

    def create_branch(self, name):
        path = f'.cvs\\refs\\heads\\{name}'
        branch = self.branch_handler.get_head_branch()
        if branch is None:
            commit = self.branch_handler.get_head_commit()
        else:
            commit = self.branch_handler.get_commit_by_branch(branch)
        with open(path) as f:
            f.write(commit)

    def remove_branch(self, name):
        if self.branch_handler.get_head_branch() == name:
            commit = self.branch_handler.get_commit_by_branch(name)
            self.branch_handler.set_head_to_commit(commit)
        os.remove(f'{self.directory}\\.cvs\\refs\\heads\\{name}')
