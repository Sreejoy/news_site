'''
    handles any kind of file operation
'''

import os

#returns the home folder
def get_home_folder():
    return os.path.expanduser('~')