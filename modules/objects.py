import pickle
import os
from modules.utilities import get_hash, read_index


class Blob:
    def __init__(self, repository, content):
        self.hash = get_hash(content)
        blob_path = f'{repository}\\.cvs\\objects\\{self.hash[:2]}'
        if not os.path.exists(blob_path):
            os.mkdir(blob_path)
        with open(f'{blob_path}\\{self.hash[2:]}', 'wb') as f:
            pickle.dump(content, f)


class Tree:
    def __init__(self, directory):
        self.index = read_index(directory)
        self.not_processed = set(self.index.keys())
        self.tree = self.build_subtree(directory)
        self.content = ''
        for line in self.tree:
            self.content += f'{line}\n'
        self.hash = Blob(directory, self.content).hash

    def build_subtree(self, path):
        tree = []
        for item in os.listdir(path):
            if '.cvs' in item:
                continue
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                if item_path in self.not_processed:
                    self.not_processed.remove(item_path)
                    tree.append(f'blob {self.index[item_path]} {item}')
            else:
                subtree = self.build_subtree(item_path)
                if len(subtree) == 0:
                    continue
                content = ''
                for line in subtree:
                    content += f'{line}\n'
                h = Blob(path, content).hash
                tree.append(f'tree {h} {item}')
        return tree
