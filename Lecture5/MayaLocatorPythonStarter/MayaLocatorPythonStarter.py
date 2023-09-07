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


class TriLocatorNode(omui.MPxLocatorNode):    
    # unique ID for node see lecture notes
    id = om.MTypeId(0xFF000002)
    size = None 
    drawDbClassification = "drawdb/geometry/TriLocatorNode"
    drawRegistrantId = "TriLocatorNode"


    def __init__(self):
        omui.MPxLocatorNode.__init__(self)

    
    @staticmethod
    def creator():
        """
        Think of this as a factory
        """
        return TriLocatorNode()
	
    @staticmethod
    def isBounded():
        return True
	
    
    def boundingBox(self):
        thisNode = self.thisMObject()
        plug  = om.MPlug(thisNode, TriLocatorNode.size)
        sizeVal=plug.asMDistance()
        multiplier = sizeVal.asCentimeters()
        tri_size=0.5
        corner1=om.MPoint(-tri_size,tri_size, -0.0)
        corner2=om.MPoint(tri_size, -tri_size, 0.0)
        corner1 = corner1 * multiplier
        corner2 = corner2 * multiplier

        return om.MBoundingBox(corner1, corner2)
    
 
    @staticmethod
    def initialize():
        # create and add a float attribute size
        size_FN = om.MFnUnitAttribute()
        TriLocatorNode.size = size_FN.create( "size", "sz", om.MFnUnitAttribute.kDistance )
        size_FN.default = om.MDistance(1.0)
        om.MPxNode.addAttribute( TriLocatorNode.size )
		

    def compute(self, plug, data):
        pass


#############################################################################
##
## Viewport 2.0 override implementation
##
#############################################################################
class TriLocatorData(om.MUserData):
    def __init__(self):
        om.MUserData.__init__(self, False) ## don't delete after draw
        self.colour_array = om.MColorArray()
        self.normal_array = om.MVectorArray()
        self.line_array = om.MPointArray()
        self.triangle_array = om.MPointArray()



class TriLocatorDrawOverride(omr.MPxDrawOverride):
    # // Tri Data
    # //       V2 
    # //
    # //  V1       V3

    scale = 0.5
    triangle = (  (-scale, -scale, 0.0),(0.0,scale,0.0),(scale,-scale, 0.0))


    @staticmethod
    def creator(obj):
        return TriLocatorDrawOverride(obj)

    def __init__(self, obj):
        omr.MPxDrawOverride.__init__(self, obj, None, False)

		## We want to perform custom bounding box drawing
		## so return True so that the internal rendering code
		## will not draw it for us.
        self.mCustomBoxDraw = True
        self.mCurrentBoundingBox = om.MBoundingBox()

    def supportedDrawAPIs(self):
        ## this plugin supports both GL and DX
        return omr.MRenderer.kOpenGL | omr.MRenderer.kDirectX11 | omr.MRenderer.kOpenGLCoreProfile

    def isBounded(self, objPath, cameraPath):
        return True

    def boundingBox(self, objPath, cameraPath):

        tri_size=0.5
        corner1=om.MPoint(-tri_size,tri_size, -0.0)
        corner2=om.MPoint(tri_size, -tri_size, 0.0)

        multiplier = self.getMultiplier(objPath)
        corner1 *= multiplier
        corner2 *= multiplier

        self.mCurrentBoundingBox.clear()
        self.mCurrentBoundingBox.expand( corner1 )
        self.mCurrentBoundingBox.expand( corner2 )

        return self.mCurrentBoundingBox

    def disableInternalBoundingBoxDraw(self):
        return self.mCustomBoxDraw
    
    def getMultiplier(self, objPath):
		## Retrieve value of the size attribute from the node
        node = objPath.node()
        plug = om.MPlug(node, TriLocatorNode.size)
        if not plug.isNull:
            sizeVal = plug.asMDistance()
            return sizeVal.asCentimeters()

        return 1.0


    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        ## Retrieve data cache (create if does not exist)
        data = oldData
        if not isinstance(data, TriLocatorData):
            data = TriLocatorData()
        multiplier = self.getMultiplier(objPath)
        data.line_array.clear()
        # line 1
        data.line_array.append([self.triangle[0][0] * multiplier, self.triangle[0][1] * multiplier, self.triangle[0][2] * multiplier])
        data.line_array.append([self.triangle[1][0] * multiplier, self.triangle[1][1] * multiplier, self.triangle[1][2] * multiplier])

        # line 2
        data.line_array.append([self.triangle[1][0] * multiplier, self.triangle[1][1] * multiplier, self.triangle[1][2] * multiplier])
        data.line_array.append([self.triangle[2][0] * multiplier, self.triangle[2][1] * multiplier, self.triangle[2][2] * multiplier])

        # line 3
        data.line_array.append([self.triangle[2][0] * multiplier, self.triangle[2][1] * multiplier, self.triangle[2][2] * multiplier])
        data.line_array.append([self.triangle[0][0] * multiplier, self.triangle[0][1] * multiplier, self.triangle[0][2] * multiplier])

        data.triangle_array.clear()

        data.triangle_array.append([self.triangle[0][0] * multiplier, self.triangle[0][1] * multiplier, self.triangle[0][2] * multiplier])
        data.triangle_array.append([self.triangle[1][0] * multiplier, self.triangle[1][1] * multiplier, self.triangle[1][2] * multiplier])
        data.triangle_array.append([self.triangle[2][0] * multiplier, self.triangle[2][1] * multiplier, self.triangle[2][2] * multiplier])
        # per vertex normals

        normal=om.MVector(0.0, 0.0, 1.0)
        data.normal_array.clear()
        data.normal_array.append(normal)
        data.normal_array.append(normal)
        data.normal_array.append(normal)
        data.colour_array.clear()

        data.colour_array.append(om.MColor([1.0,0.0,0.0]))
        data.colour_array.append(om.MColor([0.0,1.0,0.0]))
        data.colour_array.append(om.MColor([0.0,0.0,1.0]))
        return data
    
    def hasUIDrawables(self):
        return True


    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        locator_data = data
        if not isinstance(locator_data, TriLocatorData):
            return

        drawManager.beginDrawable()
        
        drawManager.setDepthPriority(5)

        if (frameContext.getDisplayStyle() & omr.MFrameContext.kGouraudShaded):
            drawManager.mesh(omr.MGeometry.kTriangles, locator_data.triangle_array,locator_data.normal_array, locator_data.colour_array)
        else :   
            drawManager.mesh(omr.MUIDrawManager.kLineStrip, locator_data.line_array, locator_data.normal_array, locator_data.colour_array)

        ## Draw a text "Foot"
        pos = om.MPoint( 0.0, 0.0, 0.0 )  ## Position of the text
        textColor = om.MColor( (0.1, 0.8, 0.8, 1.0) )  ## Text color

        drawManager.setColor( textColor )
        drawManager.setFontSize( omr.MUIDrawManager.kSmallFontSize )
        drawManager.text(pos, "A Trianlgle", omr.MUIDrawManager.kCenter )

        drawManager.endDrawable()





def initializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        plugin.registerNode("TriLocatorNode", TriLocatorNode.id, TriLocatorNode.creator, TriLocatorNode.initialize,om.MPxNode.kLocatorNode, TriLocatorNode.drawDbClassification)
    except:
        sys.stderr.write("Failed to register node\n")
        raise

    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(TriLocatorNode.drawDbClassification, TriLocatorNode.drawRegistrantId, TriLocatorDrawOverride.creator)
    except:
        sys.stderr.write("Failed to register override\n")
        raise


#
# UNINITIALIZES THE PLUGIN BY DEREGISTERING THE COMMAND AND NODE:
#
def uninitializePlugin(obj):
	plugin = om.MFnPlugin(obj)
	try:
		plugin.deregisterNode(TriLocatorNode.id)
	except:
		sys.stderr.write("Failed to deregister node\n")
		raise
	try:
		omr.MDrawRegistry.deregisterDrawOverrideCreator(TriLocatorNode.drawDbClassification, TriLocatorNode.drawRegistrantId)
	except:
		sys.stderr.write("Failed to deregister override\n")
		pass

    

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
    cmds.file(rename=f"{location}/NodeTest.ma")
    # now to test the node works by creating it and setting an attributes
    cmds.createNode("TriLocatorNode",name="TriLocatorNode")
    assert cmds.objExists("TriLocatorNode")==True
    cmds.setAttr("TriLocatorNode.size", 2.0)
    assert cmds.getAttr("TriLocatorNode.size")==2.0
    # now save the scene with the node in it
    cmds.file(save=True, de=False, type="mayaAscii")
    maya.standalone.uninitialize()

