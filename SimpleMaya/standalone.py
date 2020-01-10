from __future__ import print_function
import os,atexit
import maya.standalone

def exitMaya() :
    print('closing down maya')
    maya.standalone.uninitialize()

atexit.register(exitMaya)
maya.standalone.initialize(name='python')
os.system('clear')
print('Maya Python Standalone Terminal initialized')


