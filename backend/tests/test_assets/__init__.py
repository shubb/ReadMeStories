import os

def GetTestEpubPath():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, 'Worm.epub')