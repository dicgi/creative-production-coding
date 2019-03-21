'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: AUG/05/2013
.....................................................................................................
This tool generates normal based on parallel transport method and Frenet-Serret frames.
To create this tool just follow the next steps:

1 - Create new asset... (File/New Asset...);
2 - Put a operator name and a operator label as you want;
3 - Select "Python Type" on Operator Style;
4 - On Network Type, select "Geometry" (this is a very important step!!! pay attention =));
5 - Save where you want; (do not forget to put ".otl" extension, not ".py")
6 - On Type Properties window, in Code tab, paste the code below.

If you have any comments send to: diegodci@gmail.com
Thank you! :D
.....................................................................................................
References:

HANSON, A.J.; MA, Hui. Parallel Transport Approach to Curve Framing. Department of Computer Science,
Indiana University, 1995.
<http://www.cs.indiana.edu/pub/techreports/TR425.pdf>

YAMAGUCHI, Fujio. Curves and Surfaces in Computer Aided Geometric Design. Springer, 1988.
..................................................................................................'''
import math

###################
# Node initiation #
###################
node = hou.pwd()
geo = node.geometry()

#############
# Functions #
#############
def makeTemplate():
    '''
    Create node parameters
    '''
    pGroup = hou.ParmTemplateGroup()
    type = hou.MenuParmTemplate('type', 'normal type', ('tangent', 'binormal', 'normal'))
    inv = hou.ToggleParmTemplate('inv', 'invert', 0)
    pGroup.append(type)
    pGroup.append(inv)
    node.setParmTemplateGroup(pGroup)

def retTangent(points):
    '''
    Returns a list of tangents
    T(s) = x'(s)/||x'(s)||
    '''
    tanList = []
    for i in range(len(points)):
        if(i == 0):
            po = points[i].attribValue('P')
            pi = points[i + 1].attribValue('P')
        elif(i == len(points) - 1):
            po = points[i - 1].attribValue('P')
            pi = points[i].attribValue('P')
        else:
            po = points[i - 1].attribValue('P')
            pi = points[i + 1].attribValue('P')
        tan = difference(pi, po)
        tanList.append(tan)
    return tanList

def retBinormal(tanList):
    '''
    Returns a list of binormals
    B(s) = (x'(s) X x''(s))/||x'(s) X x''(s)||
    '''
    binList = []
    for i in range(len(tanList)):
        if(i == 0):
            tano = tanList[i]
            tani = tanList[i + 1]
        elif(i == len(points) - 1):
            tano = tanList[i - 1]
            tani = tanList[i]
        else:
            tano = tanList[i - 1]
            tani = tanList[i + 1]
        bin = cross(tani, tano)
        binList.append(bin)
    return binList

def retNormal(tanList, binList):
    '''
    Returns a list of normals
    N(s) = B(s) X T(s)
    '''
    normList = []
    for i in range(len(binList)):
        norm = cross(binList[i], tanList[i])
        normList.append(norm)
    return normList

def difference(v1, v2):
    '''
    Calculates a derivative differentiation between two vectors
    '''
    dx = v2[0] - v1[0]
    dy = v2[1] - v1[1]
    dz = v2[2] - v1[2]
    d = (dx, dy, dz)
    return d

def normalize(v):
    '''
    Normalize a vector. 
    The "mag" variable represents magnitude or length of vector
    '''
    v = (v[0], v[1], v[2])
    mag = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2) + math.pow(v[2], 2))
    if(mag == 0.0): mag = 0.001
    return ((v[0])/mag, v[1]/mag, v[2]/mag)

def cross(v1, v2):
    '''
    Makes a cross product between two vectors
    '''
    vx = v1[1]*v2[2] - v1[2]*v2[1]
    vy = v1[2]*v2[0] - v1[0]*v2[2]
    vz = v1[0]*v2[1] - v1[1]*v2[0]
    return (vx, vy, vz)

def invert(v):
    '''
    Invert vector
    '''
    return (-v[0], -v[1], -v[2])

########
# Main #
########
makeTemplate()

points = geo.points()

type = node.parm('type').eval()
inv = node.parm('inv').eval()

if not geo.findPointAttrib('N'):
    geo.addAttrib(hou.attribType.Point, 'N', (0.0, 1.0, 0.0))

tanList = retTangent(points)

if(type == 0):
    for i in range(len(tanList)):
        tan = normalize(tanList[i])
        if(inv == 1):
            tan = invert(tan)
        points[i].setAttribValue('N', tan)

elif(type == 1):
    binList = retBinormal(tanList)
    for i in range(len(binList)):
        bin = normalize(binList[i])
        if(inv == 1):
            bin = invert(bin)
        points[i].setAttribValue('N', bin)

else:
    binList = retBinormal(tanList)
    normList = retNormal(tanList, binList)
    for i in range(len(normList)):
        norm = normalize(normList[i])
        if(inv == 1):
            norm = invert(norm)
        points[i].setAttribValue('N', norm)