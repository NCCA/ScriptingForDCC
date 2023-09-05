import maya.api.OpenMaya as om
import maya.cmds as cmds
import math
import random
import os

def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass


maya_useNewAPI = True

name_flag_short="-n"
name_flag_long="-name"
radius_flag_short="-r"
radius_flag_long="-radius"
number_lights_flag_short="-nl"
number_lights_flag_long="-nlights"
hemisphere_flag_short="-h"
hemisphere_flag_long="-hemisphere"

# types here https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=MAYA_API_REF_py_ref_class_open_maya_1_1_m_syntax_html


def command_syntax():
    syntax = om.MSyntax()
    syntax.addFlag(name_flag_short, name_flag_long, om.MSyntax.kString)
    syntax.addFlag(radius_flag_short, radius_flag_long, om.MSyntax.kDouble)
    syntax.addFlag(number_lights_flag_short, number_lights_flag_long, om.MSyntax.kUnsigned)
    syntax.addFlag(hemisphere_flag_short, hemisphere_flag_long, om.MSyntax.kBoolean)
    return syntax




class LightOnSphere(om.MPxCommand):



    CMD_NAME = "LightOnSphere"

    def _random_point_on_sphere(self,radius : float=1.0 , hemisphere: bool=False):
        xiTheta = random.uniform(0, 1)
        temp = 2.0 * radius * math.sqrt(xiTheta * (1.0 - xiTheta))
        twoPiXiPhi = math.pi * 2 * random.uniform(0, 1)
        x = temp * math.cos(twoPiXiPhi)
        y = temp * math.sin(twoPiXiPhi)
        if hemisphere is True:
            y = abs(y)
        z = radius * (1.0 - 2.0 * xiTheta)
        return x, y, z



    def __init__(self):
        super(LightOnSphere, self).__init__()
        
    def doIt(self, args):
        """
        Called when the command is executed in script
        """
        number_of_lights=100
        radius=1.0
        hemisphere=False
        light_name="LightOnSphere"
        # Parse the arguments.
        arg_data = om.MArgParser(self.syntax(), args)
        if arg_data.isFlagSet(name_flag_short):
            light_name = arg_data.flagArgumentString(name_flag_short, 0)
        if arg_data.isFlagSet(radius_flag_short):
            radius = arg_data.flagArgumentDouble(radius_flag_short, 0)
        if arg_data.isFlagSet(number_lights_flag_short):
            number_of_lights = arg_data.flagArgumentInt(number_lights_flag_short, 0)
        if arg_data.isFlagSet(hemisphere_flag_short):
            hemisphere = arg_data.flagArgumentBool(hemisphere_flag_short, 0)

        for i in range(number_of_lights):
            name=cmds.shadingNode("pointLight", asLight=True)
            x, y, z = self._random_point_on_sphere(radius, hemisphere)
            cmds.move(x, y, z)
            cmds.rename("pointLight1", f"{light_name}_{i+1}")

    @classmethod
    def creator(cls):
        """
        Think of this as a factory
        """
        return LightOnSphere()
    


def initializePlugin(plugin):
    """
    Load our plugin
    """
    vendor = "NCCA"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(LightOnSphere.CMD_NAME, LightOnSphere.creator,command_syntax)
    except:
        om.MGlobal.displayError(f"Failed to register command: {LightOnSphere.CMD_NAME}")


def uninitializePlugin(plugin):
    """
    Exit point for a plugin
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(LightOnSphere.CMD_NAME)
    except:
        om.MGlobal.displayError(f"Failed to deregister command: {LightOnSphere.CMD_NAME}")


if __name__ == "__main__":   
    import maya.standalone
    import maya.api.OpenMaya as om
    import maya.cmds as cmds
    maya.standalone.initialize(name="python")
    cmds.loadPlugin(__file__)
    print(f"Loading plugin: {__file__}")
    cmds.file(f=True, new=True)
    location=os.getcwd()
    cmds.file(rename=f"{location}/LightOnSphere.ma")
    cmds.LightOnSphere()
    cmds.file(save=True, de=False, type="mayaAscii")
    maya.standalone.uninitialize()

