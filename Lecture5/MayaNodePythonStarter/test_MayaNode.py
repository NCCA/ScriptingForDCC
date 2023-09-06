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
