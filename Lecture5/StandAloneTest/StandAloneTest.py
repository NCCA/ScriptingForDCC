#!/usr/bin/env mayapy

import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.standalone

def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass


maya_useNewAPI = True


class HelloMaya(om.MPxCommand):

    CMD_NAME = "HelloMayaPy"

    def __init__(self):
        super(HelloMaya, self).__init__()

    def doIt(self, args):
        """
        Called when the command is executed in script
        """
        print("This should come from the python shell")
        om.MGlobal.displayWarning("This should be a warning")
        om.MGlobal.displayError("This should be an error")
        om.MGlobal.displayInfo("This should be an info message")

    @classmethod
    def creator(cls):
        """
        Think of this as a factory
        """
        return HelloMaya()


def initializePlugin(plugin):
    """
    Load our plugin
    """
    vendor = "NCCA"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(HelloMaya.CMD_NAME, HelloMaya.creator)
    except:
        om.MGlobal.displayError(f"Failed to register command: {HelloMaya.CMD_NAME}")


def uninitializePlugin(plugin):
    """
    Exit point for a plugin
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(HelloMaya.CMD_NAME)
    except:
        om.MGlobal.displayError(f"Failed to deregister command: {HelloMaya.CMD_NAME}")


if __name__ == "__main__":
    plugin_name = "HelloMaya.py"
    maya.standalone.initialize(name="python")
    cmds.loadPlugin(__file__)
    print(f"Loading plugin: {__file__}")
    cmds.HelloMayaPy()
    maya.standalone.uninitialize()

