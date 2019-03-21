'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: JULY/31/2013
.....................................................................................................
This operator makes a polygon connection between all points that are at a distance less than the 
parameter 'Radius'. To create this tool just follow the next steps:

1 - Create new operator... (File/New Operator Type...);
2 - Put a operator name and a operator label as you want;
3 - Select "Python Type" on Operator Style;
4 - On Network Type, select "Geometry Operator"(this is a very important step!!! pay attention =));
5 - Save where you want; (do not forget to put ".otl" extension, not ".py")
6 - On Type Properties window, in Code tab, paste the code below.

If you have any comments send to: diegodci@gmail.com
Thank you! :D
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
    rad = hou.FloatParmTemplate('radius', 'Radius', 1)
    pGroup.append(rad)
    node.setParmTemplateGroup(pGroup)

def distance(p1, p2):
    '''
    Calculates euclidean distance between two points.
    '''
    dx = math.pow(p2[0] - p1[0], 2)
    dy = math.pow(p2[1] - p1[1], 2)
    dz = math.pow(p2[2] - p1[2], 2)
    d = math.sqrt(dx + dy + dz)
    return d

########
# Main #
########
makeTemplate()

points = geo.points()
blackList = {}

radius = node.parm('radius').eval()

for point in points:
    blackList[point] = []

for i in range(len(points)):
    po = points[i].attribValue('P')
    for j in range(len(points)):
        if((j == i) or (j in blackList[points[i]])): continue
        pi = points[j].attribValue('P')
        dist = distance(po, pi)
        if(dist <= radius):
            line = geo.createPolygon()
            line.addVertex(points[i])
            line.addVertex(points[j])
            line.setIsClosed(False)
            blackList[points[j]].append(i)