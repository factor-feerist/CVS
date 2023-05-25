import sys
import unittest
import os
import shutil
import re

from shell import CVSShell

shell = CVSShell()


class Test_CVS(unittest.TestCase):
    def SetUp(self):
        pass




    def test_commit(self):
        directory = os.getcwd()
        shell.do_cd('test')
        shell.do_init('')
        shell.do_touch(f'{directory}\\test\\a.txt')
        shell.do_touch(f'{directory}\\test\\b.txt')
        with open(f'{directory}\\a.txt', 'w') as f:
            f.write('test1')
        with open(f'{directory}\\b.txt', 'w') as f:
            f.write('test2')
        shell.do_add('.')
        shell.do_commit('sdv')


if __name__ == "__main__":
    unittest.main()




