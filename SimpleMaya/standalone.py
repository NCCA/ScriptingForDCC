from __future__ import print_function
import os,atexit
import maya.standalone

def exitMaya() :
    print('closing down maya-standalone')
    maya.standalone.uninitialize()

atexit.register(exitMaya)
maya.standalone.initialize(name='python')
os.system('clear')
print('Maya Python Standalone Terminal initialized')
print('note : please use python3 print() functions')

