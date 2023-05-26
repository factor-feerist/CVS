import os
import pickle
import queue
import stat
from datetime import datetime
from modules.utilities import read_index
from modules.objects import Blob, Tree
from modules.branch_handler import BranchHandler


class CVS:
    def __init__(self, directory):
        self.directory = directory
        self.branch_handler = BranchHandler(directory)

    def init(self):
        os.mkdir(f'{self.directory}\\.cvs')
        os.mkdir(f'{self.directory}\\.cvs\\objects')
        os.mkdir(f'{self.directory}\\.cvs\\refs')
        os.mkdir(f'{self.directory}\\.cvs\\refs\\heads')
        os.mkdir(f'{self.directory}\\.cvs\\refs\\tags')
        with open(f'{self.directory}\\.cvs\\HEAD', 'w') as f:
            f.write('ref:refs/heads/master')
        with open(f'{self.directory}\\.cvs\\index', 'w'):
            pass
        with open(f'{self.directory}\\.cvs\\stagelog', 'w'):
            pass
        with open(f'{self.directory}\\.cvs\\commitlog', 'w'):
            pass
        with open(f'{self.directory}\\.cvs\\taglog', 'w'):
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
                f.write(f'{datetime.now().strftime("%d/%m/%y %H:%M:%S")}'
                        f'\\\\CHANGED\\\\{path}\\\\{d[path]}\\\\{h}\n')
                d[path] = h
        elif path not in d.keys():
            d[path] = h
            with open(f'{self.directory}\\.cvs\\stagelog', 'a') as f:
                f.write(f'{datetime.now().strftime("%d/%m/%y %H:%M:%S")}'
                        f'\\\\ADDED\\\\{path}\\\\{d[path]}\n')

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
        h = Blob(self.directory, commit).hash

        with open(f'{self.directory}\\.cvs\\commitlog') as f:
            clog = f.read()
        with open(f'{self.directory}\\.cvs\\commitlog', 'a') as f:
            f.write(f'Commit\\\\{h}\\\\'
                    f'{datetime.now().strftime("%d/%m/%y %H:%M:%S")}'
                    f'\\\\{message}\n')
            if parent is not None:
                prev_log = clog[clog.index(parent)::]
            d = read_index(self.directory)
            removed_log = []
            added_log = []
            changed_log = []
            not_changed_log = []
            for item in d.keys():
                if item in removed:
                    removed_log.append(f'  - {item} removed\n')
                elif parent is None:
                    added_log.append(f'  - {item} added {d[item]}\n')
                elif d[item] not in prev_log:
                    if item in prev_log:
                        changed_log.append(f'  - {item} changed {d[item]}\n')
                    else:
                        added_log.append(f'  - {item} added {d[item]}\n')
                else:
                    not_changed_log.append(f'  - {item} {d[item]}\n')
            for record in removed_log:
                f.write(record)
            for record in added_log:
                f.write(record)
            for record in changed_log:
                f.write(record)
            for record in not_changed_log:
                f.write(record)
        with open(f'{self.directory}\\.cvs\\index', 'w') as f:
            for key, value in d.items():
                if key not in removed:
                    f.write(f'{key}\\\\{value}\n')
        if branch is None:
            self.branch_handler.set_head_to_commit(h)
        else:
            self.branch_handler.set_commit_by_branch(branch, h)
        return h

    def commit_log(self):
        with open(f'{self.directory}\\.cvs\\commitlog') as f:
            return f.read()

    def create_branch(self, name):
        path = f'{self.directory}\\.cvs\\refs\\heads\\{name}'
        if os.path.exists(path):
            raise Exception(f'Branch {name} already exists')
        branch = self.branch_handler.get_head_branch()
        if branch is None:
            commit = self.branch_handler.get_head_commit()
        else:
            commit = self.branch_handler.get_commit_by_branch(branch)
        if commit is None:
            raise Exception('No commits in repository')
        with open(path, 'w') as f:
            f.write(commit)

    def remove_branch(self, name):
        if self.branch_handler.get_head_branch() == name:
            commit = self.branch_handler.get_commit_by_branch(name)
            self.branch_handler.set_head_to_commit(commit)
        path = f'{self.directory}\\.cvs\\refs\\heads\\{name}'
        if os.path.exists(path):
            os.remove(path)
        else:
            raise Exception(f'No branch named {name}')

    def create_tag(self, name, message):
        path = f'{self.directory}\\.cvs\\refs\\tags\\{name}'
        if os.path.exists(path):
            raise Exception(f'Tag {name} already exists')
        branch = self.branch_handler.get_head_branch()
        if branch is None:
            commit = self.branch_handler.get_head_commit()
        else:
            commit = self.branch_handler.get_commit_by_branch(branch)
        if commit is None:
            raise Exception('No commits in repository')
        with open(path, 'w') as f:
            f.write(f'{commit}\\\\{message}')
        with open(f'{self.directory}\\.cvs\\taglog', 'a') as f:
            f.write(f'{name}\\\\{commit}\\\\{message}\n')

    def remove_tag(self, name):
        path = f'{self.directory}\\.cvs\\refs\\tags\\{name}'
        if os.path.exists(path):
            os.remove(path)
        else:
            raise Exception(f'No tag named {name}')
        tag_log = ''
        with open(f'{self.directory}\\.cvs\\taglog') as f:
            for line in f:
                if line.split('\\\\')[0] != name:
                    tag_log += line
        with open(f'{self.directory}\\.cvs\\taglog', 'w') as f:
            f.write(tag_log)

    def tag_log(self):
        with open(f'{self.directory}\\.cvs\\taglog') as f:
            return f.read()

    def checkout(self, to):
        h = ''
        if os.path.exists(f'{self.directory}\\.cvs\\refs\\heads\\{to}'):
            with open(f'{self.directory}\\.cvs\\refs\\heads\\{to}') as f:
                h = f.read()
            self.branch_handler.set_head_to_branch(to)
        elif os.path.exists(f'{self.directory}\\.cvs\\refs\\tags\\{to}'):
            with open(f'{self.directory}\\.cvs\\refs\\tags\\{to}') as f:
                h = f.read().split('\\\\')[0]
            self.branch_handler.set_head_to_commit(h)
        elif len(to) >= 3:
            if os.path.exists(f'{self.directory}\\.cvs\\objects\\'
                              f'{to[0:2]}\\{to[2::]}'):
                h = to
                self.branch_handler.set_head_to_commit(h)
            else:
                raise Exception(f'No commit {to}')

        for item in os.listdir('.'):
            path = f'{self.directory}\\{item}'
            if os.path.isdir(path) and item != '.cvs':
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        filename = os.path.join(root, name)
                        os.chmod(filename, stat.S_IWUSR)
                        os.remove(filename)
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(path)
            elif os.path.isfile(path):
                os.remove(path)

        with open(f'{self.directory}\\.cvs\\objects\\'
                  f'{h[0:2]}\\{h[2::]}', 'rb') as f:
            commit = pickle.load(f).split('\n')[0].split()[1]
        q = queue.Queue()
        actual_files = {}
        with open(f'{self.directory}\\.cvs\\objects\\'
                  f'{commit[0:2]}\\{commit[2::]}', 'rb') as f:
            content = pickle.load(f)
        for line in content.split('\n'):
            ops = line.split()
            if len(ops) == 3:
                q.put([ops[0], ops[1], f'{ops[2]}'])
        while not q.empty():
            blob_type, h, name = q.get()
            with open(f'{self.directory}\\.cvs\\objects\\{h[0:2]}\\{h[2::]}',
                      'rb') as f:
                content = pickle.load(f)
            if blob_type == 'tree':
                os.mkdir(f'{self.directory}\\{name}')
                for line in content.split('\n'):
                    ops = line.split()
                    if len(ops) == 3:
                        q.put([ops[0], ops[1], f'{name}\\{ops[2]}'])
            elif blob_type == 'blob':
                with open(f'{self.directory}\\{name}', 'w')as f:
                    f.write(content)
                    actual_files[f'{self.directory}\\{name}'] = h

        with open(f'{self.directory}\\.cvs\\index', 'w') as f:
            for key, value in actual_files.items():
                f.write(f'{key}\\\\{value}\n')
