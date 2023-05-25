import sys
import unittest
import os
import shutil
import re
from shell import CVSShell
import stat
sys.path.append('../')



shell = CVSShell()

def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))


class TestCVS(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        directory = os.getcwd()
        shell.do_mkdir('test')
        shell.do_cd('test')
        shell.do_init('')
        self.assertTrue(os.path.isdir(f'{directory}\\test\\.cvs'))
        self.assertTrue(os.path.isdir(f'{directory}\\test\\.cvs\\objects'))
        self.assertTrue(os.path.isdir(f'{directory}\\test\\.cvs\\refs'))
        self.assertTrue(os.path.isfile(f'{directory}\\test\\.cvs\\commitlog'))
        self.assertTrue(os.path.isfile(f'{directory}\\test\\.cvs\\HEAD'))
        self.assertTrue(os.path.isfile(f'{directory}\\test\\.cvs\\index'))
        self.assertTrue(os.path.isfile(f'{directory}\\test\\.cvs\\stagelog'))
        self.assertTrue(os.path.isdir(f'{directory}\\test\\.cvs\\refs\\heads'))
        #os.system('rmdir /S /Q "{}"'.format(f'{directory}\\test'))
        #os.remove(f'{directory}\\test')
        rmtree(f'{directory}\\test')
        shell.do_cd(directory)

    def test_add(self):
        directory = os.getcwd()
        shell.do_mkdir('test')
        shell.do_cd('test')
        shell.do_init('')
        shell.do_touch('a.txt')
        shell.do_touch("b.txt")
        with open(f'{directory}\\test\\a.txt', 'w') as f:
            f.write('1')
        with open(f'{directory}\\test\\b.txt', 'w') as f:
            f.write('2')
        shell.do_mkdir("dir")
        shell.do_cd(f'{directory}\\test\\dir')
        shell.do_touch('adir.txt')
        shell.do_touch('bdir.txt')
        with open(f'{directory}\\test\\dir\\adir.txt', 'w') as f:
            f.write("1dir")
        with open(f'{directory}\\test\\dir\\bdir.txt', 'w') as f:
            f.write("2dir")
        shell.do_cd(f'{directory}\\test')
        shell.do_add('dir')
        with open(f'{directory}\\test\\dir\\adir.txt', 'w') as f:
            f.write('test1')
        shell.do_add('dir a.txt')
        with open(f'{directory}\\test\\a.txt', 'w') as f:
            f.write('test2')
        shell.do_add('.')
        result_index = []
        with open(f'{directory}\\test\\.cvs\\index', 'r') as f:
            _index = f.read().split('\n')[:-1]
            for line in _index:
                result_index.append(line.split('\\\\')[-1])
        result_log = []
        with open(f'{directory}\\test\\.cvs\\stagelog', 'r') as f:
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
        shell.do_cd(directory)
        rmtree(f'{directory}\\test')

    def test_commit(self):
        directory = os.getcwd()
        shell.do_cd('test')
        shell.do_init('')
        shell.do_touch(f'{directory}\\test\\a.txt')
        shell.do_touch(f'{directory}\\test\\b.txt')
        with open(f'{directory}\\test\\a.txt', 'w') as f:
            f.write('test1')
        with open(f'{directory}\\test\\b.txt', 'w') as f:
            f.write('test2')
        shell.do_add('.')
        shell.do_commit('test')
        self.assertTrue(os.path.isfile(f'{directory}\\test\\.cvs\\objects\\b4\\44ac06613fc8d63795be9ad0beaf55011936ac'))
        self.assertTrue(os.path.isfile(f'{directory}\\test\\.cvs\\objects\\83\\8572438ff69f29a18f35a10327460d2fde7fea'))
        self.assertTrue(os.path.isfile(f'{directory}\\test\\.cvs\\objects\\10\\9f4b3c50d7b0df729d299bc6f8e9ef9066971f'))
        self.assertTrue(os.path.isfile(f'{directory}\\test\\.cvs\\objects\\02\\082a7f163d181e9fcbe8ac11b9e6ad2aa4d6cf'))
        with open(f'{directory}\\test\\.cvs\\commitlog', 'r') as f:
            result_fl = f.readline().split('\\\\')
            self.assertEqual(result_fl[0], 'Commit')
            self.assertEqual(result_fl[1], '838572438ff69f29a18f35a10327460d2fde7fea')
            self.assertEqual(result_fl[3], 'test\n')
            result_sl = f.readline().split(' ')
            self.assertEqual(result_sl[4], 'added')
            self.assertEqual(result_sl[5], 'b444ac06613fc8d63795be9ad0beaf55011936ac\n')
            result_tl = f.readline().split(' ')
            self.assertEqual(result_tl[4], 'added')
            self.assertEqual(result_tl[5], '109f4b3c50d7b0df729d299bc6f8e9ef9066971f\n')
        shell.do_cd(directory)
        rmtree(f"{directory}\\test")




if __name__ == "__main__":
    unittest.main()




