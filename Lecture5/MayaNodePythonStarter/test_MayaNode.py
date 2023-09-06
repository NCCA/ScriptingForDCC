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