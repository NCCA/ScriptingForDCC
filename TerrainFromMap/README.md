# Terrain from Maps

These demos use maps downloaded from [https://terrain.party/](https://terrain.party/) to create meshes for maya and houdini.

The maya version uses the MImage class which has been wrapped up using the python API a write up of this can be found [here](http://jonmacey.blogspot.com/2011/04/using-maya-mscriptutil-class-in-python.html)

There is also a mayapy standalone version which will export an Obj file instead.

The Houdini demo uses hython to read an image using PIL then save houdini geo files.