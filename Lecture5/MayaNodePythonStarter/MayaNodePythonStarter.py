import maya.api.OpenMaya as om
import maya.cmds as cmds
import sys

def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass


maya_useNewAPI = True


class SimpleNode(om.MPxNode):    
    # unique ID for node see lecture notes
    id = om.MTypeId(0xFF000000)
    float_attr = None 
    string_attr = None
    bool_attr = None
    color_attr = None
    matrix_attr = None  
    time_attr = None    
    angle_attr = None
    time_attr = None
    enum_attr = None
    ramp_attr = None
    curve_ramp_attr = None
	
	
    @staticmethod
    def _set_attr_default( attr_FN):
        attr_FN.storable = True # save in file
        attr_FN.keyable = True # show in channel box
        attr_FN.readable = True # can be read by user
        attr_FN.writable = True # can be set by user


    def __init__(self):
        om.MPxNode.__init__(self)

    def postConstructor(self):
        """This method is called after the node has been created and we can
        do any initialisation here. In this case we want to create a ramp with some 
        default values
        """
        # grab this instance of the node
        this_node = self.thisMObject()
        # now we want the ramp attribute for our colours
        plug  = om.MPlug(this_node, SimpleNode.ramp_attr)
        # grab the ramp attribute by creating a ramp object
        ramp=om.MRampAttribute(plug)
        # The maya api is really this bad, we need to create arrays
        # then stuff them with values and then pass them to the ramp addEntries
        # method. It would be so nice if 
        values=om.MIntArray([0,1,2])
        colours=om.MColorArray([om.MColor((1.0, 0.0, 0.0, 1.0)),
                                om.MColor((0.0, 1.0, 0.0, 1.0)),
                                om.MColor((0.0, 0.0, 1.0, 1.0))])
        interp=om.MIntArray([om.MRampAttribute.kSmooth]*3)
        ramp.addEntries(values,colours,interp)


    
    @staticmethod
    def creator():
        """
        Think of this as a factory
        """
        return SimpleNode()
 
    @staticmethod
    def initialize():
        # create and add a float attribute
        float_attrFN = om.MFnNumericAttribute()
        SimpleNode.float_attr = float_attrFN.create("float_attr", "fa", om.MFnNumericData.kDouble, 0.0)
        SimpleNode._set_attr_default(float_attrFN)
        om.MPxNode.addAttribute(SimpleNode.float_attr)
		# create and add a string attribute
        string_attrFN = om.MFnTypedAttribute()
        SimpleNode.string_attr = string_attrFN.create("string_attr", "sa", om.MFnData.kString)
        SimpleNode._set_attr_default(string_attrFN)
        om.MPxNode.addAttribute(SimpleNode.string_attr)

        # create and add a boolean attribute
        bool_attrFN = om.MFnNumericAttribute()
        SimpleNode.bool_attr = bool_attrFN.create("bool_attr", "ba", om.MFnNumericData.kBoolean, 0)
        SimpleNode._set_attr_default(bool_attrFN)
        om.MPxNode.addAttribute(SimpleNode.bool_attr)
        # create and add a color attribute
        color_attrFN = om.MFnNumericAttribute()
        SimpleNode.color_attr = color_attrFN.createColor("color_attr", "ca")
        SimpleNode._set_attr_default(color_attrFN)
        om.MPxNode.addAttribute(SimpleNode.color_attr)

        #create a matrix attribute
        matrix_attrFN = om.MFnMatrixAttribute()
        SimpleNode.matrix_attr = matrix_attrFN.create("matrix_attr", "ma", om.MFnMatrixAttribute.kDouble)
        SimpleNode._set_attr_default(matrix_attrFN)
        om.MPxNode.addAttribute(SimpleNode.matrix_attr)
		
        # Add angle attribute
        angle_attrFN = om.MFnUnitAttribute()
        SimpleNode.angle_attr = angle_attrFN.create("angle_attr", "aa", om.MFnUnitAttribute.kAngle, 0.0)
        SimpleNode._set_attr_default(angle_attrFN)
        om.MPxNode.addAttribute(SimpleNode.angle_attr)
		
        # add a time attribute
        time_attrFN = om.MFnUnitAttribute()
        SimpleNode.time_attr = time_attrFN.create("time_attr", "ta", om.MFnUnitAttribute.kTime, 0.0)
        SimpleNode._set_attr_default(time_attrFN)
        om.MPxNode.addAttribute(SimpleNode.time_attr)
		
        # add an enum attribute
        enum_attrFN = om.MFnEnumAttribute()
        SimpleNode.enum_attr = enum_attrFN.create("enum_attr", "ea", 0)
        enum_attrFN.addField("Option 1", 0)
        enum_attrFN.addField("Option 2", 1)
        enum_attrFN.addField("Option 3", 2)
        SimpleNode._set_attr_default(enum_attrFN)
        om.MPxNode.addAttribute(SimpleNode.enum_attr)
		
        # create a ramp attribute
        ramp_attrFN = om.MRampAttribute()
        SimpleNode.ramp_attr = ramp_attrFN.createColorRamp("ramp_attr", "ra")		
        om.MPxNode.addAttribute(SimpleNode.ramp_attr)
		
        # create a curve ramp
        curve_ramp_attrFN = om.MRampAttribute()
        SimpleNode.curve_ramp_attr = curve_ramp_attrFN.createCurveRamp("curve_ramp_attr", "cra")
        om.MPxNode.addAttribute(SimpleNode.curve_ramp_attr)
		
		

    def compute(self, plug, data):
        pass


def initializePlugin(obj):
	plugin = om.MFnPlugin(obj)
	try:
		plugin.registerNode("SimpleNode", SimpleNode.id, SimpleNode.creator, SimpleNode.initialize)
	except:
		sys.stderr.write("Failed to register node\n")
		raise

#
# UNINITIALIZES THE PLUGIN BY DEREGISTERING THE COMMAND AND NODE:
#
def uninitializePlugin(obj):
	plugin = om.MFnPlugin(obj)

	try:
		plugin.deregisterNode(SimpleNode.id)
	except:
		sys.stderr.write("Failed to deregister node\n")
		raise

    

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
    cmds.createNode("SimpleNode",name="SimpleNode")
    assert cmds.objExists("SimpleNode")==True
    cmds.setAttr("SimpleNode.float_attr", 1.0)
    assert cmds.getAttr("SimpleNode.float_attr")==1.0
    cmds.setAttr("SimpleNode.string_attr", "Hello World", type="string")
    assert cmds.getAttr("SimpleNode.string_attr")=="Hello World"
    cmds.setAttr("SimpleNode.bool_attr", 1)
    assert cmds.getAttr("SimpleNode.bool_attr")==True
	# set the colour attribute
    cmds.setAttr("SimpleNode.color_attr", 1.0, 0.0, 0.0, type="double3")
    assert cmds.getAttr("SimpleNode.color_attr")[0][0]==1.0
    assert cmds.getAttr("SimpleNode.color_attr")[0][1]==0.0
    assert cmds.getAttr("SimpleNode.color_attr")[0][2]==0.0
	
    # set the matrix attribute
    # create a matrix
    matrix = om.MMatrix()
    # set the matrix to the identity matrix
    matrix.setToIdentity()
    # set the matrix attribute  
    cmds.setAttr("SimpleNode.matrix_attr", matrix, type="matrix")
    # get the matrix attribute
    matrix = cmds.getAttr("SimpleNode.matrix_attr") 
    
    # now test the matrix is correct as simple identity should be ok for float compare
    result=[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    assert matrix==result
	
    # test the angle attribute
    cmds.setAttr("SimpleNode.angle_attr", 90.0)
    assert cmds.getAttr("SimpleNode.angle_attr")==90.0
	
    # test the time attribute
    cmds.setAttr("SimpleNode.time_attr", 10.0)
    assert cmds.getAttr("SimpleNode.time_attr")==10.0
	
    # test the enum attribute
    cmds.setAttr("SimpleNode.enum_attr", 1)
    assert cmds.getAttr("SimpleNode.enum_attr")==1
	
    

    # now save the scene with the node in it
    cmds.file(save=True, de=False, type="mayaAscii")
    maya.standalone.uninitialize()

