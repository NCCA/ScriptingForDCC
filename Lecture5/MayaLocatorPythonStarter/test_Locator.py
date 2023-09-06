import pytest

import maya.standalone
import maya.api.OpenMaya as om
import maya.cmds as cmds
import pathlib

import sys

def setup_module(module):
    maya.standalone.initialize(name="python")
    location = pathlib.Path().absolute()

    cmds.loadPlugin(f"{location}/MayaLocatorPythonStarter.py")
    cmds.createNode("TriLocator",name="TriLocator")



def teardown_module(module):
    cmds.delete("TriLocator")
    assert cmds.objExists("TriLocator")==False
    maya.standalone.uninitialize()


def test_createNode():
    assert cmds.objExists("TriLocator")==True
