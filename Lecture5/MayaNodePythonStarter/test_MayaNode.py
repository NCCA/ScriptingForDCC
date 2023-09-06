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


def teardown_module(module):
    maya.standalone.uninitialize()


def test_createNode():
    cmds.createNode("SimpleNode",name="SimpleNode")
    assert cmds.objExists("SimpleNode")==True
    cmds.delete("SimpleNode")

def test_float_attr():
    cmds.createNode("SimpleNode",name="SimpleNode")
    cmds.setAttr("SimpleNode.float_attr", 1.0)
    assert cmds.getAttr("SimpleNode.float_attr")==1.0
    cmds.delete("SimpleNode")
