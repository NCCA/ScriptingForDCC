import pytest

import maya.standalone
import maya.api.OpenMaya as om
import maya.cmds as cmds
import pathlib

import sys

def setup_module(module):
    maya.standalone.initialize(name="python")
    location = pathlib.Path().absolute()

    cmds.loadPlugin(f"{location}/MayaNodePythonStarter.py")
    cmds.createNode("SimpleNode",name="SimpleNode")



def teardown_module(module):
    cmds.delete("SimpleNode")
    assert cmds.objExists("SimpleNode")==False
    maya.standalone.uninitialize()


def test_createNode():
    assert cmds.objExists("SimpleNode")==True

def test_float_attr():
    cmds.setAttr("SimpleNode.float_attr", 1.0)
    assert cmds.getAttr("SimpleNode.float_attr")==1.0

def test_string_attr():
    cmds.setAttr("SimpleNode.string_attr", "Hello World", type="string")
    assert cmds.getAttr("SimpleNode.string_attr")=="Hello World"

def test_bool_attr():
    cmds.setAttr("SimpleNode.bool_attr", 1)
    assert cmds.getAttr("SimpleNode.bool_attr")==True

def test_color_attr():
    cmds.setAttr("SimpleNode.color_attr", 1.0, 0.0, 0.0, type="double3")
    assert cmds.getAttr("SimpleNode.color_attr")[0][0]==1.0
    assert cmds.getAttr("SimpleNode.color_attr")[0][1]==0.0
    assert cmds.getAttr("SimpleNode.color_attr")[0][2]==0.0

def test_matrix_attr():
    # create a matrix
    matrix = om.MMatrix()
    # set the matrix to the identity matrix
    matrix.setToIdentity()
    # set the matrix attribute  
    cmds.setAttr("SimpleNode.matrix_attr", matrix, type="matrix")
    # get the matrix attribute
    matrix = cmds.getAttr("SimpleNode.matrix_attr") 
    
    # now test the matrix is correct as simple identity should be ok for float compare
    result=[1.0, 0.0, 0.0, 0.0, 
            0.0, 1.0, 0.0, 0.0, 
            0.0, 0.0, 1.0, 0.0, 
            0.0, 0.0, 0.0, 1.0]
    assert matrix==result

def test_angle_attr():
    cmds.setAttr("SimpleNode.angle_attr", 90.0)
    assert cmds.getAttr("SimpleNode.angle_attr")==90.0

def test_time_attr():
    cmds.setAttr("SimpleNode.time_attr", 10.0)
    assert cmds.getAttr("SimpleNode.time_attr")==10.0


def test_enum_attr():
    cmds.setAttr("SimpleNode.enum_attr", 1)
    assert cmds.getAttr("SimpleNode.enum_attr")==1


