'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: AUG/12/2013
.....................................................................................................
This tool makes smoothly transfer of point attributes between two models. To create this tool just
follow the next steps:

1 - Create new operator... (File/New Operator Type...);
2 - Put a operator name and a operator label as you want;
3 - Select "Python Type" on Operator Style;
4 - On Network Type, select "Geometry Operator"(this is a very important step!!! pay attention =));
5 - Save where you want; (do not forget to put ".otl" extension, not ".py")
6 - On Type Properties window, in Basic tab, set to 2 a minimum and maximum inputs
6 - In Code tab, paste the code below.

If you have any comments send to: diegodci@gmail.com
Thank you! :D
..................................................................................................'''
import math

###################
# Node initiation #
###################
node = hou.pwd()
geoA = node.geometry()
geoB = node.inputs()[1].geometry()

#############
# Functions #
#############
def makeTemplate():
    '''
    Create node parameters
    '''
    pGroup = hou.ParmTemplateGroup()
    ttype = hou.MenuParmTemplate('ttype', 'transfer type', ('over', 'add'))
    selAttrib = hou.ToggleParmTemplate('selAttrib', 'Selected Attributes', 1)
    attList = hou.StringParmTemplate('attList', 'Attribute List', 1)
    attList.setDefaultValue('*')
    minrad = hou.FloatParmTemplate('minrad', 'Minimum Radius', 1)
    maxrad = hou.FloatParmTemplate('maxrad', 'Maximum Radius', 1, (5.0, 0.0, 0.0))
    gain = hou.FloatParmTemplate('gain', 'Gain', 1, (1.0, 0.0, 0.0), 0.0, 1.0)
    igamma = hou.FloatParmTemplate('igamma', 'Interpolation Gamma', 1, (1.0, 0.0, 0.0), 0.0, 4.0)
    matPos = hou.ToggleParmTemplate('matPos', 'Match Position', 0)
    pGroup.append(ttype)
    pGroup.append(selAttrib)
    pGroup.append(attList)
    pGroup.append(minrad)
    pGroup.append(maxrad)
    pGroup.append(gain)
    pGroup.append(igamma)
    pGroup.append(matPos)
    node.setParmTemplateGroup(pGroup)

def distance(p1, p2):
    '''
    Calculate euclidean distance between two points.
    '''
    dx = math.pow(p2[0] - p1[0], 2)
    dy = math.pow(p2[1] - p1[1], 2)
    dz = math.pow(p2[2] - p1[2], 2)
    d = math.sqrt(dx + dy + dz)
    return d

def sumVectors(v1, v2):
    '''
    Add two vectors
    '''
    vx = v1[0] + v2[0]
    vy = v1[1] + v2[1]
    vz = v1[2] + v2[2]
    return (vx, vy, vz)

def multVecFloat(v, f):
    '''
    Multiply a vector by a float
    '''
    vx = v[0]*f
    vy = v[1]*f
    vz = v[2]*f
    return (vx, vy, vz)

def defaultValues(dataType):
    '''
    Returns a value of zero depending a type of the attribute.
    '''
    if(dataType == tuple): return (0.0, 0.0, 0.0)
    elif(dataType == float): return 0.0
    elif(dataType == int): return 0
    else: return ''

########
# Main #
########
makeTemplate()

pointsA = geoA.points()
pointsB = geoB.points()

ttype = node.parm('ttype').eval()
selAttrib = node.parm('selAttrib').eval()
attList = node.parm('attList').eval()
minrad = node.parm('minrad').eval()
maxrad = node.parm('maxrad').eval()
gain = node.parm('gain').eval()
igamma = node.parm('igamma').eval()
matPos = node.parm('matPos').eval()

if(attList == '*'):
    if(selAttrib == 1):
        attribs = list(geoB.pointAttribs())
        for i in range(len(attribs)):
            attribs[i] = attribs[i].name()
    else:
        attribs = []
elif(attList == ''):
    if(selAttrib == 0):
        attribs = list(geoB.pointAttribs())
        for i in range(len(attribs)):
            attribs[i] = attribs[i].name()
    else:
        attribs = []
else:
    attribs = list(geoB.pointAttribs())
    for i in range(len(attribs)):
            attribs[i] = attribs[i].name()
    attList = attList.split(',')
    for i in range(len(attList)):
            attList[i] = attList[i].strip()
    if(selAttrib == 1):
        dnes = []
        for att in attList:
            if(att not in attribs):
                dnes.append(att)
        for dne in dnes:
            print('attribute %s does not exist' %(dne))
            attList.remove(dne)
        attribs = attList
    else:
        for att in attList:
            try:
                attribs.remove(att)
            except:
                continue

if(matPos == 0):
    attribs.remove('P')
    attribs.remove('Pw')

for attrib in attribs:
    if not geoA.findPointAttrib(attrib):
        try:
            geoA.addAttrib(hou.attribType.Point, attrib, defaultValues(type(pointsB[0].attribValue(attrib))))
        except:
            None
    for pointB in pointsB:
        pb = pointB.attribValue('P')
        attribB = pointB.attribValue(attrib)
        for pointA in pointsA:
            pa = pointA.attribValue('P')
            dist = distance(pa, pb)
            if(dist > maxrad): continue
            elif(dist <= minrad): alpha = 1.0
            else:
                alpha = (dist - maxrad)/(minrad - maxrad)
            attribA = pointA.attribValue(attrib)
            oalpha = math.pow(1 - alpha, 1/igamma)*gain
            aalpha = math.pow(alpha, 1/igamma)*gain
            if(type(attribB) == tuple):
                if(ttype == 0):
                    attribA = sumVectors(multVecFloat(attribB, aalpha), multVecFloat(attribA, oalpha))
                else:
                    attribA = sumVectors(multVecFloat(attribB, aalpha), attribA)
            elif(type(attribB) == int):
                if(ttype == 0):
                    attribA = int(attribB*aalpha + attribA*(oalpha))
                else:
                    attribA += int(attribB*aalpha)
            else:
                if(ttype == 0):
                    attribA = attribB*aalpha + attribA*(oalpha)
                else:
                    attribA += attribB*alpha
            pointA.setAttribValue(attrib, attribA)