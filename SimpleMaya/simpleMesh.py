#!/opt/autodesk/maya/bin/mayapy

from __future__ import print_function
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.standalone


def buildMesh() :

  numVertices=4
  numFaces=1
  outputMesh = OpenMaya.MObject()
  points = OpenMaya.MFloatPointArray()
  faceConnects = OpenMaya.MIntArray()
  faceCounts = OpenMaya.MIntArray()
  p = OpenMaya.MFloatPoint(-1.0,0.0,-1.0)
  points.append(p)
  p = OpenMaya.MFloatPoint(-1.0,0.0,1.0)
  points.append(p)
  p = OpenMaya.MFloatPoint(1.0,0.0,1.0)
  points.append(p)
  p = OpenMaya.MFloatPoint(1.0,0.0,-1.0)
  points.append(p)
  faceConnects.append(0)
  faceConnects.append(1)
  faceConnects.append(2)
  faceConnects.append(3)
  faceCounts.append(4)

  meshFN = OpenMaya.MFnMesh()
  print ("create Mesh")
  meshFN.create(4, 1, points, faceCounts, faceConnects, outputMesh)
  nodeName = meshFN.name()
  print(nodeName)
  cmds.sets(nodeName, add='initialShadingGroup')  
  cmds.select(nodeName)  
  meshFN.updateSurface()

if __name__ == '__main__':
  maya.standalone.initialize(name='python')
  buildMesh()