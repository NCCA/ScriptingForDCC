from __future__ import print_function,division
import maya.cmds as cmds
import maya.api.OpenMaya as om

  

def main() :
  grpPostfix='CtlGrp'
  controlPostfix='ctrl'
  dag=om.MItDag( filterType=om.MFn.kJoint)
  dagFN=om.MFnDagNode()
  # grab the selected items 
  sel=om.MGlobal.getActiveSelectionList()
  firstNode=True 
  while not dag.isDone() :
    node=dag.currentItem()
    dagFN.setObject(node) 
    ctrlName='{}{}'.format(dagFN.name(),controlPostfix)
    print(' found joint called {} '.format(dagFN.name()))
    if firstNode == True :
      parentName='{}{}'.format(dagFN.name(),grpPostfix)
      print('FirstNode ',parentName)
      cmds.group(em=True, name=parentName)
      cmds.circle(name=ctrlName)
      cmds.parent(ctrlName,parentName)
      firstNode=False  
    else :
      print(' adding group',parentName)
#      cmds.group(em=True, name='{}CTRL'.format(dagFN.name()))
      cmds.group(em=True, name='{}{}'.format(dagFN.name(),grpPostfix), parent=parentName)
      cmds.circle(name=ctrlName)
      cmds.parent(ctrlName,parentName)
      parentName='{}{}'.format(dagFN.name(),grpPostfix)

    dag.next() # move to next node


if __name__ == '__main__' :
  main()