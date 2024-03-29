#!/usr/bin/env python
from __future__ import print_function

import random

from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

import Poisson as ps


def _addModel(model, prototypesPrimPath, stage):
    # the name must be a full path without the . so just strip .usd from name
    name = model[0 : model.find(".")]
    primPath = prototypesPrimPath.AppendChild(name)
    treeRefPrim = stage.DefinePrim(primPath)
    refs = treeRefPrim.GetReferences()
    refs.AddReference(model)

    path = treeRefPrim.GetPath()

    leaves = "/World/TreePointInstance/prototypes/{}/Leaves".format(name)
    tree = UsdGeom.Mesh(stage.GetPrimAtPath(leaves))
    tree.CreateDisplayColorAttr([(0.0, 0.8, 0.0)])

    materialRoot = "/World/Leaf{}Material".format(name)
    material = UsdShade.Material.Define(stage, materialRoot)
    pbrShader = UsdShade.Shader.Define(stage, materialRoot + "/LeafShader")
    pbrShader.CreateIdAttr("UsdPreviewSurface")

    pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.2)
    pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.1)
    # material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")

    stReader = UsdShade.Shader.Define(stage, materialRoot + "/stReader")
    stReader.CreateIdAttr("UsdPrimvarReader_float2")
    # add texture
    diffuseTextureSampler = UsdShade.Shader.Define(
        stage, materialRoot + "/diffuseTexture"
    )
    diffuseTextureSampler.CreateIdAttr("UsdUVTexture")
    diffuseTextureSampler.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(
        name + "Leaves.png"
    )
    # diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
    diffuseTextureSampler.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)
    diffuseTextureSampler.CreateOutput("a", Sdf.ValueTypeNames.Float)
    # pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')
    # pbrShader.CreateInput("opacityThreshold", Sdf.ValueTypeNames.Float).ConnectToSource(diffuseTextureSampler, 'a')

    stInput = material.CreateInput("frame:stPrimvarName", Sdf.ValueTypeNames.Token)
    stInput.Set("st")
    # stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)
    UsdShade.MaterialBindingAPI(tree).Bind(material)

    trunk = "/World/TreePointInstance/prototypes/{}/Trunk".format(name)
    tree = UsdGeom.Mesh(stage.GetPrimAtPath(trunk))
    tree.CreateDisplayColorAttr([(0.5, 0.2, 0.0)])

    materialRoot = "/World/Trunk{}Material".format(name)
    material = UsdShade.Material.Define(stage, materialRoot)
    pbrShader = UsdShade.Shader.Define(stage, materialRoot + "TrunkShader")
    pbrShader.CreateIdAttr("UsdPreviewSurface")
    pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(
        (0.5, 0.2, 0.0)
    )
    pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.2)
    pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.1)
    # material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
    # add texture
    diffuseTextureSampler = UsdShade.Shader.Define(
        stage, materialRoot + "/diffuseTexture"
    )
    diffuseTextureSampler.CreateIdAttr("UsdUVTexture")
    diffuseTextureSampler.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(
        name + "Trunk.png"
    )
    # diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
    diffuseTextureSampler.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)
    # pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')

    stInput = material.CreateInput("frame:stPrimvarName", Sdf.ValueTypeNames.Token)
    stInput.Set("st")
    stReader.CreateInput("varname", Sdf.ValueTypeNames.Token).ConnectToSource(stInput)

    UsdShade.MaterialBindingAPI(tree).Bind(material)

    # return the actual path to the model which will be added to the instancer
    return path


def _addGround(stage, width, height):
    boxPrim = UsdGeom.Cube.Define(stage, "/World/ground")
    boxPrim.CreateDisplayColorAttr([(0.5, 0.2, 0.0)])
    xformable = UsdGeom.Xformable(boxPrim)
    xformable.AddScaleOp().Set(Gf.Vec3f(width / 2, 0.1, height / 2))

    material = UsdShade.Material.Define(stage, "/World/GroundMaterial")
    pbrShader = UsdShade.Shader.Define(stage, "/World/GroundMaterial/GroundShader")
    pbrShader.CreateIdAttr("UsdPreviewSurface")
    pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(
        (0.5, 0.2, 0.0)
    )

    pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.9)
    pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    # material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
    # UsdShade.MaterialBindingAPI(boxPrim).Bind(material)


def main():
    width = 400
    height = 400
    r = 3.5
    k = 20
    scatter = ps.PoissonDisc(width, height, r, k)
    points = scatter.sample()

    stage = Usd.Stage.CreateNew("Forest.usda")
    world = UsdGeom.Xform.Define(stage, "/World")

    instancer = UsdGeom.PointInstancer.Define(
        stage, world.GetPath().AppendChild("TreePointInstance")
    )
    prototypesPrim = stage.DefinePrim(instancer.GetPath().AppendChild("prototypes"))
    prototypesPrimPath = prototypesPrim.GetPath()
    _addGround(stage, width, height)
    models = ["tree1.usd", "tree2.usd"]
    modelTargets = []
    for m in models:
        modelTargets.append(_addModel(m, prototypesPrimPath, stage))

    positions = []
    indices = []
    rotations = []
    w2 = width / 2
    h2 = height / 2
    rot = Gf.Rotation()
    for _, point in enumerate(points):
        positions.append(
            Gf.Vec3f(w2 - point[0], random.uniform(-0.1, 0.1), h2 - point[1])
        )
        indices.append(random.randint(0, len(models) - 1))
        rot = Gf.Rotation(Gf.Vec3d(0, 1, 0), random.uniform(0, 360))
        r = rot.GetQuaternion().GetReal()
        img = rot.GetQuaternion().GetImaginary()
        rotations.append(Gf.Quath(r, img[0], img[1], img[2]))

    instancer.CreatePositionsAttr(positions)
    instancer.CreateProtoIndicesAttr(indices)
    instancer.CreateOrientationsAttr(rotations)
    instancer.CreatePrototypesRel().SetTargets(modelTargets)

    invisibleIds = UsdGeom.PointInstancer.Get(
        stage, "/World/TreePointInstance"
    ).GetInvisibleIdsAttr()

    numTrees = len(points)
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(numTrees)
    frame = 0
    step = 1
    for _ in range(0, numTrees, step):
        hide = range(frame, len(points))
        invisibleIds.Set(hide, time=frame)
        frame = frame + step

    stage.GetRootLayer().Save()


if __name__ == "__main__":
    main()
