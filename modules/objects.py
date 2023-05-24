import pickle
import os
from modules.utilities import get_hash, read_index


class Blob():
    def __init__(self, repository, content):
        self.hash = get_hash(content)
        blob_path = f'{repository}\\.cvs\\objects\\{self.hash[:2]}'
        if not os.path.exists(blob_path):
            os.mkdir(blob_path)
        with open(f'{blob_path}\\{self.hash[2:]}', 'wb') as f:
            f.write(self.serialize())

    def serialize(self):
        return pickle.dumps(self)
        

class Tree():
    def __init__(self, directory):
        self.directory = directory
        self.index = read_index(directory)
        self.not_processed = self.index.keys()
        self.tree = self.build_subtree(directory)
        self.content = ''
        for line in tree:
            self.content += f'{line}\n'
        self.hash = Blob(self.directory, self.content).hash
        

    def build_subtree(self, path):
        tree = []
        for item in os.listdir(directory):
            if '.cvs' in item:
                continue
            path = os.path.join(directory, item)
            if os.path.isfile(path):
                if path in self.not_processed:
                    self.not_processed.remove(path)
                    tree.append(f'blob {self.index[path]} {item}')
            else:
                subtree = build_subtree(path)
                if len(subtree) == 0:
                    continue
                content = ''
                for line in subtree:
                    content += f'{line}\n'
                h = Blob(self.directory, content).hash
                tree.append(f'tree {h} {item}')
        
        return tree
