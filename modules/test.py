import sys
import unittest
import os
import shutil
import re
sys.path.append('../')
from shell import CVSShell

shell = CVSShell()


class TestCVS(unittest.TestCase):
    def SetUp(self):
        pass

    def test_init(self):
        directory = os.getcwd()
        shell.do_init('')
        directory = os.path.join(directory, '.cvs')
        self.assertTrue(os.path.isdir(directory))
        self.assertTrue(os.path.isdir(f'{directory}\\objects'))
        self.assertTrue(os.path.isdir(f'{directory}\\refs'))
        self.assertTrue(os.path.isfile(f'{directory}\\commitlog'))
        self.assertTrue(os.path.isfile(f'{directory}\\HEAD'))
        self.assertTrue(os.path.isfile(f'{directory}\\index'))
        self.assertTrue(os.path.isfile(f'{directory}\\stagelog'))
        self.assertTrue(os.path.isdir(f'{directory}\\refs\\heads'))
        shutil.rmtree(directory)
        shell.do_cd(directory)

    def test_add(self):
        directory = os.path.join(os.getcwd(), 'test')
        shell.do_cd('test')
        shell.do_init('')
        shell.do_touch('a.txt')
        shell.do_touch("b.txt")
        with open(f'{directory}\\a.txt', 'w') as f:
            f.write('1')
        with open(f'{directory}\\b.txt', 'w') as f:
            f.write('2')
        shell.do_mkdir("dir")
        shell.do_cd(os.path.join(directory, 'dir'))
        shell.do_touch('adir.txt')
        shell.do_touch('bdir.txt')
        with open(f'{directory}\\dir\\adir.txt', 'w') as f:
            f.write("1dir")
        with open(f'{directory}\\dir\\bdir.txt', 'w') as f:
            f.write("2dir")
        shell.do_cd(directory)
        shell.do_add('dir')
        with open(os.path.join(os.path.join(directory, 'dir'),
                               'adir.txt'), 'w') as f:
            f.write('test1')
        shell.do_add('dir a.txt')
        with open(os.path.join(directory, 'a.txt'), 'w') as f:
            f.write('test2')
        shell.do_add('.')
        result_index = []
        with open(f'{directory}\\.cvs\\index', 'r') as f:
            _index = f.read().split('\n')[:-1]
            for line in _index:
                result_index.append(line.split('\\\\')[-1])
        result_log = []
        with open(f'{directory}\\.cvs\\stagelog', 'r') as f:
            for line in f.read().split('\n')[:-1]:
                result_log.append(str(line.split('\\\\')[-1]))
        unittest.TestCase.assertEqual(self, result_index,
                                      ['b444ac06613fc8d63795'
                                       'be9ad0beaf55011936ac',
                                       '5839faba624c7c7b58c7'
                                       '1033446dfc7a55f63bbf',
                                       '109f4b3c50d7b0df729d'
                                       '299bc6f8e9ef9066971f',
                                       'da4b9237bacccdf19c07'
                                       '60cab7aec4a8359010b0'])
        unittest.TestCase.assertEqual(self, result_log,
                                      ['9334405ce86ccd5a82eb'
                                       'df09ed7c2047a654599c',
                                       '5839faba624c7c7b58c7'
                                       '1033446dfc7a55f63bbf',
                                       'b444ac06613fc8d63795'
                                       'be9ad0beaf55011936ac',
                                       '356a192b7913b04c5457'
                                       '4d18c28d46e6395428ab',
                                       '109f4b3c50d7b0df729d'
                                       '299bc6f8e9ef9066971f',
                                       'da4b9237bacccdf19c07'
                                       '60cab7aec4a8359010b0'])
        shutil.rmtree(f'{directory}\\.cvs')
        shutil.rmtree(f'{directory}\\dir')
        os.remove(f'{directory}\\a.txt')
        os.remove(f'{directory}\\b.txt')

    def test_commit(self):
        directory = os.path.join(os.getcwd(), 'test')
        shell.do_cd('test')
        shell.do_init('')
        shell.do_touch(f'{directory}\\a.txt')
        shell.do_touch(f'{directory}\\b.txt')
        with open(f'{directory}\\a.txt', 'w') as f:
            f.write('test1')
        with open(f'{directory}\\b.txt', 'w') as f:
            f.write('test2')
        shell.do_add('.')
        shell.do_commit('sdv')
        self.assertTrue(os.path.isfile(f'{directory}\\.cvs\\objects\\b4\\44ac06613fc8d63795be9ad0beaf55011936ac'))
        with open(f'{directory}\\.cvs\\objects\\b4\\44ac06613fc8d63795be9ad0beaf55011936ac') as f:
            self.assertEqual(f.readline(),
            'Ђ•U       Њmodules.objects”ЊBlob”“”)Ѓ”}”Њhash”Њ(b444ac06613fc8d63795be9ad0beaf55011936ac”sb.')
        self.assertTrue(os.path.isfile(f'{directory}\\.cvs\\objects\\93\\bc5fa433afe94a7b10dd955df6e80c91b25961'))
        with open(f'{directory}\\.cvs\\objects\\93\\bc5fa433afe94a7b10dd955df6e80c91b25961') as f:
            self.assertEqual(f.readline(),
            'Ђ•U       Њmodules.objects”ЊBlob”“”)Ѓ”}”Њhash”Њ(93bc5fa433afe94a7b10dd955df6e80c91b25961”sb.')
        self.assertTrue(os.path.isfile(f'{directory}\\.cvs\\objects\\10\\9f4b3c50d7b0df729d299bc6f8e9ef9066971f'))
        with open(f'{directory}\\.cvs\\objects\\10\\9f4b3c50d7b0df729d299bc6f8e9ef9066971f') as f:
            self.assertEqual(f.readline(),
            'Ђ•U       Њmodules.objects”ЊBlob”“”)Ѓ”}”Њhash”Њ(109f4b3c50d7b0df729d299bc6f8e9ef9066971f”sb.')
        self.assertTrue(os.path.isfile(f'{directory}\\.cvs\\objects\\02\\082a7f163d181e9fcbe8ac11b9e6ad2aa4d6cf'))
        with open(f'{directory}\\.cvs\\objects\\02\\082a7f163d181e9fcbe8ac11b9e6ad2aa4d6cf') as f:
            self.assertEqual(f.readline(),
            'Ђ•U       Њmodules.objects”ЊBlob”“”)Ѓ”}”Њhash”Њ(02082a7f163d181e9fcbe8ac11b9e6ad2aa4d6cf”sb.')
        shutil.rmtree(f'{directory}\\.cvs')
        os.remove(f'{directory}\\a.txt')
        os.remove(f'{directory}\\b.txt')



if __name__ == "__main__":
    unittest.main()




