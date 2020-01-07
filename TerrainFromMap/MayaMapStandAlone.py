#!/opt/autodesk/maya/bin/mayapy
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.standalone
import argparse


class MayaImage :
	""" The main class, needs to be constructed with a filename """
	def __init__(self,filename) :
		""" constructor pass in the name of the file to load (absolute file name with path) """
		# create an MImage object
		self.image=OpenMaya.MImage()
		# read from file MImage should handle errors for us so no need to check
		self.image.readFromFile(filename)
		# as the MImage class is a wrapper to the C++ module we need to access data
		# as pointers, to do this use the MScritUtil helpers
		scriptUtilWidth = OpenMaya.MScriptUtil()
		scriptUtilHeight = OpenMaya.MScriptUtil()

		# first we create a pointer to an unsigned in for width and height
		widthPtr = scriptUtilWidth.asUintPtr()
		heightPtr = scriptUtilHeight.asUintPtr()
		# now we set the values to 0 for each
		scriptUtilWidth.setUint( widthPtr, 0 )
		scriptUtilHeight.setUint( heightPtr, 0 )
		# now we call the MImage getSize method which needs the params passed as pointers
		# as it uses a pass by reference
		self.image.getSize( widthPtr, heightPtr )
		# once we get these values we need to convert them to int so use the helpers
		self.m_width = scriptUtilWidth.getUint(widthPtr)
		self.m_height =scriptUtilHeight.getUint(heightPtr)
		# now we grab the pixel data and store
		self.charPixelPtr = self.image.pixels()
		# query to see if it's an RGB or RGBA image, this will be True or False
		self.m_hasAlpha=self.image.isRGBA()
		# if we are doing RGB we step into the image array in 3's
		# data is always packed as RGBA even if no alpha present
		self.imgStep=4
		# finally create an empty script util and a pointer to the function
		# getUcharArrayItem function for speed
		scriptUtil = OpenMaya.MScriptUtil()
		self.getUcharArrayItem=scriptUtil.getUcharArrayItem


	def width(self) :
		""" return the width of the image """
		return self.m_width

	def height(self) :
		""" return the height of the image """
		return self.m_height

	def hasAlpha(self) :
		""" return True is the image has an Alpha channel """
		return self.m_hasAlpha

	def getPixel(self,x,y) :
		""" get the pixel data at x,y and return a 3/4 tuple depending upon type """
		# check the bounds to make sure we are in the correct area
		if x<0 or x>self.m_width :
			print "error x out of bounds\n"
			return
		if y<0 or y>self.m_height :
			print "error y our of bounds\n"
			return
		# now calculate the index into the 1D array of data
		index=(y*self.m_width*4)+x*4
		# grab the pixels
		red = self.getUcharArrayItem(self.charPixelPtr,index)
		green = self.getUcharArrayItem(self.charPixelPtr,index+1)
		blue = self.getUcharArrayItem(self.charPixelPtr,index+2)
		alpha=self.getUcharArrayItem(self.charPixelPtr,index+3)
		return (red,green,blue,alpha)

	def getRGB(self,x,y) :
		r,g,b,_=self.getPixel(x,y)
		return (r,g,b)


def create(verts, faces, merge=True):
    '''
    Given a list of vertices (iterables of floats) and a list of faces (iterable of integer vert indices),
    creates and returns a maya Mesh
    '''

    cmds.select(cl=True)  
    outputMesh = OpenMaya.MObject()

    numFaces = len(faces)
    numVertices = len(verts)

    # point array of plane vertex local positions
    points = OpenMaya.MFloatPointArray()
    for eachVt in verts:
        p = OpenMaya.MFloatPoint(eachVt[0], eachVt[1], eachVt[2])
        points.append(p)

    # vertex connections per poly face in one array of indexs into point array given above
    faceConnects = OpenMaya.MIntArray()
    for eachFace in faces:
        for eachCorner in eachFace:
            faceConnects.append(int(eachCorner))

    # an array to hold the total number of vertices that each face has
    faceCounts = OpenMaya.MIntArray()
    for c in range(0, numFaces, 1):
        faceCounts.append(int(4))

    # create mesh object using arrays above and get name of new mesh
    meshFN = OpenMaya.MFnMesh()
    """
    print numVertices,numFaces
    print points
    print faceCounts
    print faceConnects
    """
    newMesh = meshFN.create(numVertices, numFaces, points, faceCounts, faceConnects, outputMesh)
    nodeName = meshFN.name()
    cmds.sets(nodeName, add='initialShadingGroup')  
    cmds.select(nodeName)  
    meshFN.updateSurface()
    # this is useful because it deletes stray vertices (ie, those not used in any faces)
    if merge:
        cmds.polyMergeVertex(nodeName, ch=0)
    meshFN.updateSurface()
    return nodeName


def main(filename,outname,width,height) :


	img=MayaImage(filename)


	verts = []
	faces = []
	cmds.constructionHistory(tgl = 'off')

	faceIndex=int(0)
	xstep=width/float(img.width())
	zstep=height/float(img.height())
	
	sz=-height/2.0
	h=img.height()
	w=img.width()


	for y in range(0,h-1) :
		sx=-width/2.0
		for x in range(0,w) :
			pixel1=img.getRGB(x,y)
			pixel2=img.getRGB(x,y+1)
			pixel3=img.getRGB(x+1,y)
			pixel4=img.getRGB(x+1,y+1)

			verts.append((sx,float(pixel1[0])*0.1,sz))
			verts.append((sx,float(pixel2[0])*0.1,sz+zstep))
			verts.append((sx+xstep,float(pixel4[0])*0.1,sz+zstep))
			verts.append((sx+xstep,float(pixel3[0])*0.1,sz))
			sx+=xstep
			faces.append((faceIndex,faceIndex+1,faceIndex+2,faceIndex+3))
			faceIndex+=4
		sz+=zstep

	create(verts,faces)
	#cmds.select(all=True)
	cmds.file(outname,type="OBJexport",pr=True,es=True)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='turn map into mesh')

	parser.add_argument('--inputfile', '-i', nargs='?', type=str, required=True,
											help='input map name')

	parser.add_argument('--outputfile', '-o', nargs='?', type=str, required=True,
											help='output file name')


	parser.add_argument('--width', '-w', nargs='?', type=float, default=20.0,
												help='width of output mesh')

	parser.add_argument('--depth', '-d', nargs='?', type=float, default=20.0,
												help='depth of output mesh')

	args = parser.parse_args()
	maya.standalone.initialize(name='python')
	cmds.loadPlugin('objExport')
	main(args.inputfile,args.outputfile,args.width,args.depth)