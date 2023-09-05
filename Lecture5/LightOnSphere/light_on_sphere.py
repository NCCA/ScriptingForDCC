import math
import random
import maya.cmds as cmds


def random_point_on_sphere(radius : float=1.0 , hemisphere: bool=False):
    xiTheta = random.uniform(0, 1)
    temp = 2.0 * radius * math.sqrt(xiTheta * (1.0 - xiTheta))
    twoPiXiPhi = math.pi * 2 * random.uniform(0, 1)
    x = temp * math.cos(twoPiXiPhi)
    y = temp * math.sin(twoPiXiPhi)
    if hemisphere is True:
        y = abs(y)
    z = radius * (1.0 - 2.0 * xiTheta)
    return x, y, z


def scatter_lights(nlights : int=100, radius : float=10.0, hemisphere : bool=True, base_name : str="light"):
    for i in range(nlights):
        name = cmds.shadingNode("pointLight", asLight=True)
        x, y, z = random_point_on_sphere(radius, hemisphere)
        cmds.move(x, y, z)
        cmds.rename("pointLight1", base_name + "_" + str(i + 1))


scatter_lights()
