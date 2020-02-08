from __future__ import print_function,division
import maya.cmds as cmds
import maya.api.OpenMaya as om


dag=om.MItDag( filterType=om.MFn.kJoint)
dagFN=om.MFnDagNode()
# grab the selected items 
sel=om.MGlobal.getActiveSelectionList() 
print(sel)
while not dag.isDone() :
  node=dag.currentItem()
  dagFN.setObject(node) 
  print(' found joint called {} '.format(dagFN.name()))
  dag.next() # move to next node
