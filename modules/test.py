import sys
import unittest
import os
import stat
sys.path.append('../')
from shell import CVSShell


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
        self.directory = os.getcwd()
        self.shell = CVSShell()
        self.repository = os.path.join(self.directory, 'test')

    def test_init(self):
        self.shell.do_mkdir('test')
        self.shell.do_cd('test')
        self.shell.do_init('')
        self.assertTrue(os.path.isdir(f'{self.repository}\\.cvs'))
        self.assertTrue(os.path.isdir(f'{self.repository}\\.cvs\\objects'))
        self.assertTrue(os.path.isdir(f'{self.repository}\\.cvs\\refs'))
        self.assertTrue(os.path.isfile(f'{self.repository}\\.cvs\\commitlog'))
        self.assertTrue(os.path.isfile(f'{self.repository}\\.cvs\\HEAD'))
        self.assertTrue(os.path.isfile(f'{self.repository}\\.cvs\\index'))
        self.assertTrue(os.path.isfile(f'{self.repository}\\.cvs\\stagelog'))
        self.assertTrue(os.path.isdir(f'{self.repository}\\.cvs\\refs\\heads'))
        rmtree(self.repository)
        self.shell.do_cd(self.directory)

    def test_add(self):
        self.shell.do_mkdir('test')
        self.shell.do_cd('test')
        self.shell.do_init('')
        self.shell.do_touch('a.txt')
        self.shell.do_touch("b.txt")
        with open(f'{self.repository}\\a.txt', 'w') as f:
            f.write('1')
        with open(f'{self.repository}\\b.txt', 'w') as f:
            f.write('2')
        self.shell.do_mkdir("dir")
        self.shell.do_cd(f'{self.repository}\\dir')
        self.shell.do_touch('adir.txt')
        self.shell.do_touch('bdir.txt')
        with open(f'{self.repository}\\dir\\adir.txt', 'w') as f:
            f.write("1dir")
        with open(f'{self.repository}\\dir\\bdir.txt', 'w') as f:
            f.write("2dir")
        self.shell.do_cd(self.repository)
        self.shell.do_add('dir')
        with open(f'{self.repository}\\dir\\adir.txt', 'w') as f:
            f.write('test1')
        self.shell.do_add('dir a.txt')
        with open(f'{self.repository}\\a.txt', 'w') as f:
            f.write('test2')
        self.shell.do_add('.')
        result_index = []
        with open(f'{self.repository}\\.cvs\\index', 'r') as f:
            _index = f.read().split('\n')[:-1]
            for line in _index:
                result_index.append(line.split('\\\\')[-1])
        result_log = []
        with open(f'{self.repository}\\.cvs\\stagelog', 'r') as f:
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
        self.shell.do_cd(self.directory)
        rmtree(self.repository)

    def test_commit(self):
        self.shell.do_cd('test')
        self.shell.do_init('')
        self.shell.do_touch(f'{self.repository}\\a.txt')
        self.shell.do_touch(f'{self.repository}\\b.txt')
        with open(f'{self.repository}\\a.txt', 'w') as f:
            f.write('test1')
        with open(f'{self.repository}\\b.txt', 'w') as f:
            f.write('test2')
        self.shell.do_add('.')
        self.shell.do_commit('test')
        self.assertTrue(os.path.isfile(f'{self.repository}'
                                       f'\\.cvs\\objects\\b4\\44ac06613fc8d'
                                       f'63795be9ad0beaf55011936ac'))
        self.assertTrue(os.path.isfile(f'{self.repository}'
                                       f'\\.cvs\\objects\\83\\8572438ff69f2'
                                       f'9a18f35a10327460d2fde7fea'))
        self.assertTrue(os.path.isfile(f'{self.repository}'
                                       f'\\.cvs\\objects\\10\\9f4b3c50d7b0d'
                                       f'f729d299bc6f8e9ef9066971f'))
        self.assertTrue(os.path.isfile(f'{self.repository}'
                                       f'\\.cvs\\objects\\02\\082a7f163d181'
                                       f'e9fcbe8ac11b9e6ad2aa4d6cf'))
        with open(f'{self.repository}\\.cvs\\commitlog', 'r') as f:
            result_fl = f.readline().split('\\\\')
            self.assertEqual(result_fl[0], 'Commit')
            self.assertEqual(result_fl[1], '838572438ff69f29a18f'
                                           '35a10327460d2fde7fea')
            self.assertEqual(result_fl[3], 'test\n')
            result_sl = f.readline().split(' ')
            self.assertEqual(result_sl[4], 'added')
            self.assertEqual(result_sl[5], 'b444ac06613fc8d63795'
                                           'be9ad0beaf55011936ac\n')
            result_tl = f.readline().split(' ')
            self.assertEqual(result_tl[4], 'added')
            self.assertEqual(result_tl[5], '109f4b3c50d7b0df729d'
                                           '299bc6f8e9ef9066971f\n')
        self.shell.do_cd(self.directory)
        rmtree(self.repository)

    def test_branch(self):
        self.shell.do_cd('test')
        self.shell.do_init('')
        self.shell.do_touch(f'{self.repository}\\a.txt')
        self.shell.do_touch(f'{self.repository}\\b.txt')
        with open(f'{self.repository}\\a.txt', 'w') as f:
            f.write('test1')
        with open(f'{self.repository}\\b.txt', 'w') as f:
            f.write('test2')
        self.shell.do_add('.')
        self.shell.do_commit('test')
        self.shell.do_branch('vetka')
        with open(f'{self.repository}\\.cvs\\refs\\heads\\vetka', 'r') as f:
            result = f.readline()
            self.assertEqual(result,
                             '838572438ff69f29a18f35a10327460d2fde7fea')
        self.shell.do_branch('vetka r')
        result_delete = os.path.exists(f'{self.repository}'
                                       f'\\.cvs\\refs\\heads\\vetka')
        self.assertFalse(result_delete)
        self.shell.do_cd(self.directory)
        rmtree(self.repository)


if __name__ == "__main__":
    unittest.main()
