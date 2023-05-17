import hashlib
import pickle
    

class Blob():
    def __init__(self, content):
        self.content = content

    def serialize(self):
        return pickle.dumps(self)

def get_hash(content):
    return hashlib.sha1(content.encode("utf-8")).hexdigest()

