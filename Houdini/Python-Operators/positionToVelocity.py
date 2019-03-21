'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: JULY/29/2013
.....................................................................................................
This is a very simple tool to creates a velocity point attribute from position differentiation. 
To create this tool just follow the next steps:

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
    mult = hou.FloatParmTemplate('mult', 'Multiply', 1, (1.0, 0.0, 0.0), 0.0, 4.0)
    pGroup.append(mult)
    node.setParmTemplateGroup(pGroup)

def difference(v1, v2):
    '''
    Calculates a derivative differentiation between two vectors
    '''
    dx = (v2[0] - v1[0])*mult
    dy = (v2[1] - v1[1])*mult
    dz = (v2[2] - v1[2])*mult
    d = (dx, dy, dz)
    return d

########
# Main #
########
makeTemplate()

pointsA = geoA.points()
pointsB = geoB.points()

mult = node.parm('mult').eval()

if not geoA.findPointAttrib('v'):
    try:
        geoA.addAttrib(hou.attribType.Point, 'v', (0.0, 0.0, 0.0))
    except:
        None

for i in range(len(pointsA)):
    pa = pointsA[i].attribValue('P')
    pb = pointsB[i].attribValue('P')
    v = difference(pa, pb)
    pointsA[i].setAttribValue('v', v)