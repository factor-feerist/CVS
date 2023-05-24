import os


class BranchHandler:
    def __init__(self, directory):
        self.directory = directory

    def get_head_branch(self):
        with open(f'{directory}\\.cvs\\HEAD') as f:
            head_type, head_ref = f.read().split(':')
        if head_type == 'ref':
            return head_ref.split('/')[2]
        return None

    def get_head_commit(self):
        with open(f'{directory}\\.cvs\\HEAD') as f:
            head_type, h = f.read().split(':')
        if head_type != 'ref':
            return h
        return None
        
    def get_commit_by_branch(self, branch):
        path = f'.cvs\\refs\\heads\\{branch}'
        full_path = os.path.join(directory, path)
        if os.path.exists(full_path):
            with open(full_path) as f:
                return f.read()
        return None

    def set_head_to_commit(self, commit):
        with open(f'{directory}\\.cvs\\HEAD', 'w') as f:
            f.write(f'obj:{commit}')

    def set_head_to_branch(self, branch):
        with open(f'{directory}\\.cvs\\HEAD', 'w') as f:
            f.write(f'ref:ref/heads/{branch}')

    def set_commit_by_branch(self, branch, commit):
        with open(f'{directory}\\.cvs\\refs\\heads\\{branch}', 'w') as f:
            f.write(commit)
