import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr

import maya.cmds as cmds
import sys


def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass


maya_useNewAPI = True


class CubeLocator(omui.MPxLocatorNode):
    # unique ID for node see lecture notes
    id = om.MTypeId(0xFF0000F2)
    width = None
    height = None
    depth = None
    volume = None
    drawDbClassification = "drawdb/geometry/CubeLocator"
    drawRegistrantId = "CubeLocator"

    def __init__(self):
        omui.MPxLocatorNode.__init__(self)

    @staticmethod
    def creator():
        """
        Think of this as a factory
        """
        return CubeLocator()

    @staticmethod
    def isBounded():
        return True

    def boundingBox(self):
        thisNode = self.thisMObject()
        width = om.MPlug(thisNode, CubeLocator.width)
        height = om.MPlug(thisNode, CubeLocator.height)
        depth = om.MPlug(thisNode, CubeLocator.depth)
        widthVal = width.asFloat()
        heightVal = height.asFloat()
        depthVal = depth.asFloat()

        corner1 = om.MPoint(-widthVal / 2, heightVal / 2, -depthVal / 2)
        corner2 = om.MPoint(widthVal / 2, -heightVal / 2, depthVal / 2)

        return om.MBoundingBox(corner1, corner2)

    @staticmethod
    def _set_attr_default(attr_FN):
        attr_FN.storable = True  # save in file
        attr_FN.keyable = True  # show in channel box
        attr_FN.readable = True  # can be read by user
        attr_FN.writable = True  # can be set by user

    @staticmethod
    def initialize():

        try :
            numeric_fn = om.MFnNumericAttribute()
            CubeLocator.width = numeric_fn.create(
                "width", "w", om.MFnNumericData.kDouble, 1.0
            )
            om.MPxNode.addAttribute(CubeLocator.width)
        except :
            sys.stderr.write("Failed to create width attribute\n")
            raise

        try :
            CubeLocator.height = numeric_fn.create(
                "height", "h", om.MFnNumericData.kDouble, 1.0
            )
            CubeLocator._set_attr_default(numeric_fn)
            om.MPxNode.addAttribute(CubeLocator.height)

        except :
            sys.stderr.write("Failed to create height attribute\n")
            raise

        try :
            CubeLocator.depth = numeric_fn.create(
                "depth", "d", om.MFnNumericData.kDouble, 1.0
            )
            CubeLocator._set_attr_default(numeric_fn)
            om.MPxNode.addAttribute(CubeLocator.depth)
        except :    
            sys.stderr.write("Failed to create depth attribute\n")
            raise

        try :
            # NOTE : v is used already (not sure why) so need vl for short flag
            CubeLocator.volume = numeric_fn.create(
                "volume", "vl", om.MFnNumericData.kDouble, 1.0,
            )
            numeric_fn.readable = True
            numeric_fn.writable = False
            numeric_fn.storable = False
            numeric_fn.keyable = False
            numeric_fn.channelBox = True

            om.MPxNode.addAttribute(CubeLocator.volume)
        except :
            sys.stderr.write("Failed to create volume attribute\n")
            raise
        om.MPxNode.attributeAffects(CubeLocator.width, CubeLocator.volume)
        om.MPxNode.attributeAffects(CubeLocator.height, CubeLocator.volume)
        om.MPxNode.attributeAffects(CubeLocator.depth, CubeLocator.volume)

    def compute(self, plug, data):
        if plug == CubeLocator.volume:
            dependency_fn=om.MFnDependencyNode ( self.thisMObject() )
            width=dependency_fn.findPlug("width", True)
            width=width.asDouble()
            height=dependency_fn.findPlug("height", True)
            height=height.asDouble()
            depth=dependency_fn.findPlug("depth", True)
            depth=depth.asDouble()
            volume=width*height*depth
            volume_plug=om.MPlug(self.thisMObject(), CubeLocator.volume)
            volume_plug.setDouble(volume)
            data.setClean(plug)
            # return self on success (old api used om.kSuccess)
            return self
        else:
            # return None on failure (old api used om.kUnknownParameter)
            return None
        
#############################################################################
##
## Viewport 2.0 override implementation
##
#############################################################################
class CubeLocatorData(om.MUserData):
    def __init__(self):
        om.MUserData.__init__(self, False)  ## don't delete after draw
        self.line_array = om.MPointArray()
        self.index_array = []


class CubeLocatorDrawOverride(omr.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return CubeLocatorDrawOverride(obj)

    def __init__(self, obj):
        omr.MPxDrawOverride.__init__(self, obj, None, False)

        ## We want to perform custom bounding box drawing
        ## so return True so that the internal rendering code
        ## will not draw it for us.
        self.mCustomBoxDraw = True
        self.mCurrentBoundingBox = om.MBoundingBox()

    def supportedDrawAPIs(self):
        ## this plugin supports both GL and DX
        return (
            omr.MRenderer.kOpenGL
            | omr.MRenderer.kDirectX11
            | omr.MRenderer.kOpenGLCoreProfile
        )

    def isBounded(self, objPath, cameraPath):
        return True

    def _get_w_h_d(self,objPath):
        node = objPath.node()
        width = om.MPlug(node, CubeLocator.width)
        height = om.MPlug(node, CubeLocator.height)
        depth = om.MPlug(node, CubeLocator.depth)
        widthVal = width.asFloat()
        heightVal = height.asFloat()
        depthVal = depth.asFloat()
        return widthVal,heightVal,depthVal


    def boundingBox(self, objPath, cameraPath):
        width,height,depth = self._get_w_h_d(objPath)
        corner1 = om.MPoint(-width / 2, height / 2, -depth / 2)
        corner2 = om.MPoint(width / 2, -height / 2, depth / 2)

        self.mCurrentBoundingBox.clear()
        self.mCurrentBoundingBox.expand(corner1)
        self.mCurrentBoundingBox.expand(corner2)

        return self.mCurrentBoundingBox

    def disableInternalBoundingBoxDraw(self):
        return self.mCustomBoxDraw

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        ## Retrieve data cache (create if does not exist)
        data = oldData
        if not isinstance(data, CubeLocatorData):
            data = CubeLocatorData()
        data.line_array.clear()
        width,height,depth = self._get_w_h_d(objPath)
        data.line_array.append(om.MPoint(-width/2, height/2, -depth/2))
        data.line_array.append(om.MPoint(width/2, height/2, -depth/2))
        data.line_array.append(om.MPoint(width/2, height/2, depth/2))
        data.line_array.append(om.MPoint(-width/2, height/2, depth/2))
        data.line_array.append(om.MPoint(-width/2, -height/2, -depth/2))
        data.line_array.append(om.MPoint(width/2, -height/2, -depth/2))
        data.line_array.append(om.MPoint(width/2, -height/2, depth/2))
        data.line_array.append(om.MPoint(-width/2, -height/2, depth/2))
        
        top_face = om.MUintArray([0, 1, 2, 3,0])
        bottom_face = om.MUintArray([4, 5, 6, 7,4])
        front_face = om.MUintArray([1, 5, 6, 2,1])
        back_face = om.MUintArray([0, 4, 7, 3,0])
        left_face = om.MUintArray([0, 4, 5, 1,0])
        right_face = om.MUintArray([3, 7, 6, 2,3])     
        data.indices =[top_face, bottom_face, front_face, back_face, left_face, right_face]
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        locator_data = data
        if not isinstance(locator_data, CubeLocatorData):
            return

        drawManager.beginDrawable()

        drawManager.setDepthPriority(5)
        # only draw wireframe, see TriangleLocator.py for shaded example
        for index in locator_data.indices:
            drawManager.mesh(
                omr.MUIDrawManager.kClosedLine,
                locator_data.line_array,
                index=index,
            )
        drawManager.endDrawable()


def initializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        plugin.registerNode(
            "CubeLocator",
            CubeLocator.id,
            CubeLocator.creator,
            CubeLocator.initialize,
            om.MPxNode.kLocatorNode,
            CubeLocator.drawDbClassification,
        )
    except:
        sys.stderr.write("Failed to register node\n")
        raise

    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(
            CubeLocator.drawDbClassification,
            CubeLocator.drawRegistrantId,
            CubeLocatorDrawOverride.creator,
        )
    except:
        sys.stderr.write("Failed to register override\n")
        raise


#
# UNINITIALIZES THE PLUGIN BY DEREGISTERING THE COMMAND AND NODE:
#
def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    try:
        plugin.deregisterNode(CubeLocator.id)
    except:
        sys.stderr.write("Failed to deregister node\n")
        raise
    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator(
            CubeLocator.drawDbClassification, CubeLocator.drawRegistrantId
        )
    except:
        sys.stderr.write("Failed to deregister override\n")
        pass


"""
The following code makes it easy to develop and test the maya plugin
without using maya. It is not needed for the plugin to work in maya.
"""


if __name__ == "__main__":
    """it is not advised to do imports inside the main block usually
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
    cmds.file(rename=f"{location}/NodeTest.ma")
    # now to test the node works by creating it and setting an attributes
    cmds.createNode("CubeLocator", name="CubeLocator")
    assert cmds.objExists("CubeLocator") == True
    cmds.setAttr("CubeLocator.width", 2.0)
    assert cmds.getAttr("CubeLocator.width") == 2.0

    cmds.setAttr("CubeLocator.height", 3.0)
    assert cmds.getAttr("CubeLocator.height") == 3.0

    cmds.setAttr("CubeLocator.depth", 4.0)
    assert cmds.getAttr("CubeLocator.depth") == 4.0

    assert cmds.getAttr("CubeLocator.volume") == (2.0 * 3.0 * 4.0)

    # now save the scene with the node in it
    cmds.file(save=True, de=False, type="mayaAscii")
    maya.standalone.uninitialize()
