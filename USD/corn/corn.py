#!/usr/bin/env python
from __future__ import print_function
from pxr import Usd, UsdGeom, Gf, UsdShade,Sdf
import random
import OpenImageIO as oiio





def _addModel(model,prototypesPrimPath,stage) :
  # the name must be a full path without the . so just strip .usd from name
  name=model[0:model.find('.')]
  primPath=prototypesPrimPath.AppendChild(name)
  treeRefPrim = stage.DefinePrim(primPath)
  refs = treeRefPrim.GetReferences()
  refs.AddReference(model)
  
  path=treeRefPrim.GetPath()

  # leaves='/World/TreePointInstance/prototypes/{}/Leaves'.format(name)
  # tree=UsdGeom.Mesh(stage.GetPrimAtPath(leaves))
  # tree.CreateDisplayColorAttr([(0.0,0.8,0.0)])

  # materialRoot='/World/Leaf{}Material'.format(name)
  # material = UsdShade.Material.Define(stage, materialRoot)
  # pbrShader = UsdShade.Shader.Define(stage, materialRoot+'/LeafShader')
  # pbrShader.CreateIdAttr("UsdPreviewSurface")
 
  # pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.2)
  # pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.1)
  # material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")

  # stReader = UsdShade.Shader.Define(stage, materialRoot+'/stReader')
  # stReader.CreateIdAttr('UsdPrimvarReader_float2')
  # # add texture
  # diffuseTextureSampler = UsdShade.Shader.Define(stage,materialRoot+'/diffuseTexture')
  # diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
  # diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(name+'Leaves.png')
  # diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
  # diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
  # diffuseTextureSampler.CreateOutput('a', Sdf.ValueTypeNames.Float)
  # pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')
  # pbrShader.CreateInput("opacityThreshold", Sdf.ValueTypeNames.Float).ConnectToSource(diffuseTextureSampler, 'a')
 
 
  # stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
  # stInput.Set('st')
  # stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
  # UsdShade.MaterialBindingAPI(tree).Bind(material)


  # trunk='/World/TreePointInstance/prototypes/{}/Trunk'.format(name)
  # tree=UsdGeom.Mesh(stage.GetPrimAtPath(trunk))
  # tree.CreateDisplayColorAttr([(0.5,0.2,0.0)])

  # materialRoot='/World/Trunk{}Material'.format(name)
  # material = UsdShade.Material.Define(stage, materialRoot)
  # pbrShader = UsdShade.Shader.Define(stage, materialRoot+'TrunkShader')
  # pbrShader.CreateIdAttr("UsdPreviewSurface")
  # pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.5,0.2,0.0))
  # pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.2)
  # pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.1)
  # material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
  # # add texture
  # diffuseTextureSampler = UsdShade.Shader.Define(stage,materialRoot+'/diffuseTexture')
  # diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
  # diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(name+'Trunk.png')
  # diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
  # diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
  # pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')
  
  # stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
  # stInput.Set('st')
  # stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)


  # UsdShade.MaterialBindingAPI(tree).Bind(material)S
  # return the actual path to the model which will be added to the instancer
  return path


def _addGround(stage,width,depth) :
  boxPrim = UsdGeom.Cube.Define(stage, '/World/ground')
  boxPrim.CreateDisplayColorAttr([(0.5,0.2,0.0)])
  xformable = UsdGeom.Xformable(boxPrim)
  xformable.AddScaleOp().Set(Gf.Vec3f(width,0.1,depth))


  material = UsdShade.Material.Define(stage, '/World/GroundMaterial')
  pbrShader = UsdShade.Shader.Define(stage, '/World/GroundMaterial/GroundShader')
  pbrShader.CreateIdAttr("UsdPreviewSurface")
  pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.5,0.2,0.0))
 
  pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.9)
  pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
  material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
  UsdShade.MaterialBindingAPI(boxPrim).Bind(material)


def _addCamera(stage) :
  cam = UsdGeom.Camera.Define(stage, '/World/main_cam')

  # the camera derives from UsdGeom.Xformable so we can 
  # use the XformCommonAPI on it, too, and see how rotations are handled
  xformAPI = UsdGeom.XformCommonAPI(cam)
  xformAPI.SetTranslate( (8, 1.8, 8) )
  # -86 degree rotation around X axis.  Can specify rotation order as
  # optional parameter
  xformAPI.SetRotate( (-10, 0, 0 ) )

def main() :
  stage = Usd.Stage.CreateNew('CornField.usd')
  world = UsdGeom.Xform.Define(stage, '/World')
  _addCamera(stage)
  buf = oiio.ImageBuf ( 'cropMap.png')
  spec = buf.spec()
  divisor=1
  width=spec.width/divisor
  depth=spec.height/divisor
  print("image dimensions {} {}".format(width,depth))

  instancer = UsdGeom.PointInstancer.Define(stage, world.GetPath().AppendChild('TreePointInstance'))
  prototypesPrim = stage.DefinePrim(instancer.GetPath().AppendChild('prototypes'))
  prototypesPrimPath = prototypesPrim.GetPath()
  _addGround(stage,width,depth)
  models=['corn.usd','crushedCorn.usd']
  modelTargets=[]
  for m in models :
    modelTargets.append(_addModel(m,prototypesPrimPath,stage))


  positions = []
  indices = []
  rotations=[]
  rot=Gf.Rotation()


  xstart=-width/2.0
  ystart=-depth/2.0
  print("x/y start {}{}".format(xstart,ystart))
  for y in range(0,depth/divisor) :
    for x in range(0,width/divisor) :
      pixel=buf.getpixel(x,y)
      xpos=xstart+(x)+random.uniform(-0.2,0.2)
      ypos=ystart+(y)+random.uniform(-0.2,0.2)
      xpos=xpos*0.3
      ypos=ypos*0.3
      
      positions.append(Gf.Vec3f(xpos,0,ypos))

      rot=Gf.Rotation(Gf.Vec3d(0,1,0),random.uniform(0,360))
      r=rot.GetQuaternion().GetReal()
      img=rot.GetQuaternion().GetImaginary()
      rotations.append(Gf.Quath(r,img[0],img[1],img[2]))
      if pixel[0] > 0.0 :
        indices.append(0)
      else :
        indices.append(1)
      

  instancer.CreatePositionsAttr(positions)
  instancer.CreateProtoIndicesAttr(indices)
  instancer.CreateOrientationsAttr(rotations)
  instancer.CreatePrototypesRel().SetTargets(modelTargets)


  stage.GetRootLayer().Save()   


if __name__ == '__main__':
    main()