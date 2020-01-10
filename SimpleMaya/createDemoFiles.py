#!/opt/autodesk/maya/bin/mayapy

from __future__ import print_function
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.standalone
import sys,os
def main() :
  if not os.path.isdir('./SceneFiles') :
    os.mkdir('SceneFiles')
  os.chdir('SceneFiles')
  pwd=os.getcwd()
  print('Changed to {}'.format(pwd))
  
  cmds.sphere(name='test')
  cmds.file( rename=pwd+'/fred.ma' )
  cmds.file( save=True, type='mayaAscii' )



if __name__ == '__main__':
  maya.standalone.initialize(name='python')
  main()