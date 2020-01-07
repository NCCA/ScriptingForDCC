#!/opt/autodesk/maya/bin/mayapy
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.standalone
import argparse
from MayaImage import MayaImage




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