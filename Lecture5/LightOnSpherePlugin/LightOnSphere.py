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

class LightOnSphere(om.MPxCommand):

    name_flag_short="-n"
    name_flag_long="-name"
    radius_flag_short="-r"
    radius_flag_long="-radius"
    number_lights_flag_short="-nl"
    number_lights_flag_long="-nlights"
    hemisphere_flag_short="-h"
    hemisphere_flag_long="-hemisphere"


    CMD_NAME = "LightOnSphere"

    @classmethod
    def command_syntax(cls):
        """
        This is where we define the arguments for our command
        # types here https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=MAYA_API_REF_py_ref_class_open_maya_1_1_m_syntax_html
        """
        syntax = om.MSyntax()
        syntax.addFlag(cls.name_flag_short, cls.name_flag_long, om.MSyntax.kString)
        syntax.addFlag(cls.radius_flag_short, cls.radius_flag_long, om.MSyntax.kDouble)
        # Note for int types we have two options, either unsigned or long
        # later we can parse as int
        syntax.addFlag(cls.number_lights_flag_short, cls.number_lights_flag_long, om.MSyntax.kUnsigned)
        syntax.addFlag(cls.hemisphere_flag_short, cls.hemisphere_flag_long, om.MSyntax.kBoolean)
        return syntax

    def _random_point_on_sphere(self,radius : float=1.0 , hemisphere: bool=False):
        """ generate a point on a sphere / hemispehrere
        :param radius: radius of sphere
        :param hemisphere: if true generate a point on the hemisphere
        :return: x, y, z coordinates of point
        """
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
        # set default argument values
        number_of_lights=100
        radius=1.0
        hemisphere=False
        light_name="LightOnSphere"
        # Parse the arguments.
        arg_data = om.MArgParser(self.syntax(), args)
        if arg_data.isFlagSet(self.name_flag_short):
            light_name = arg_data.flagArgumentString(self.name_flag_short, 0)
        if arg_data.isFlagSet(self.radius_flag_short):
            radius = arg_data.flagArgumentDouble(self.radius_flag_short, 0)
        if arg_data.isFlagSet(self.number_lights_flag_short):
            number_of_lights = arg_data.flagArgumentInt(self.number_lights_flag_short, 0)
        if arg_data.isFlagSet(self.hemisphere_flag_short):
            hemisphere = arg_data.flagArgumentBool(self.hemisphere_flag_short, 0)
        # Create the lights
        for i in range(number_of_lights):
            name=cmds.shadingNode("pointLight", asLight=True)
            x, y, z = self._random_point_on_sphere(radius, hemisphere)
            cmds.move(x, y, z)
            cmds.rename("pointLight1", f"{light_name}_{i+1}")

    @classmethod
    def creator(cls):
        """
        Think of this as a factory to crete an instance of our command
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
        plugin_fn.registerCommand(LightOnSphere.CMD_NAME, LightOnSphere.creator,LightOnSphere.command_syntax)
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

"""
The following code makes it easy to develop and test the maya plugin
without using maya. It is not needed for the plugin to work in maya.
"""


if __name__ == "__main__":   
    """ it is not advised to do imports inside the main block usually 
    however there is an overhead to importing maya.standalone so we only
    want to do it if we are running this file directly

    Also the imports for OpenMaya and Maya.cmds need to happen after the 
    standalone has been imported so we need them as well.
    """
    import maya.standalone
    import maya.api.OpenMaya as om
    import maya.cmds as cmds
    import pathlib
    maya.standalone.initialize(name="python")
    # here we use the __file__ dunder method to get the correct plugin file 
    # to load, if we are doing more complex development we may need to use 
    # a mod file instead. 
    cmds.loadPlugin(__file__)
    print(f"Loading plugin: {__file__}")
    # Now create a new scene for testing
    cmds.file(f=True, new=True)
    # will put it in same folder as the plugin
    location = pathlib.Path().absolute()
    cmds.file(rename=f"{location}/LightOnSphere.ma")
    # run our command
    cmds.LightOnSphere(nl=2000, r=10.0, h=True, n="TestLight")
    # now save the light
    cmds.file(save=True, de=False, type="mayaAscii")
    maya.standalone.uninitialize()

