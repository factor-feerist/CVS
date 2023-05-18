import os
import hashlib
       

def get_hash(content):
    return hashlib.sha1(content.encode("utf-8")).hexdigest()

def read_index(directory):
    if os.path.exists(f'{directory}\\.cvs\\index'):
        with open(f'{directory}\\.cvs\\index') as f:
            index = f.read()
    else:
        index = ''
    d = {}
    for line in index.split('\n'):
        ops = line.split('\\\\')
        if len(ops) == 2:
            d[ops[0]] = ops[1]
    return d
