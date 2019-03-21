'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: JAN/19/2015
.....................................................................................................
This script creates a locator to be used to control a focus distance on an arnold camera.
If you have any comment send it to: diegodci@gmail.com
Thank you! :D
..................................................................................................'''
import maya.cmds as cmds

sel = cmds.ls(selection = True, dagObjects = True, leaf = True)

for obj in sel:
    if cmds.objectType(obj) == 'camera':
        cam = cmds.pickWalk(obj, direction = 'up')
        rot = cmds.getAttr('%s.rotate' %(cam[0]))
        pos = cmds.getAttr('%s.translate' %(cam[0]))
        scl = cmds.getAttr('%s.scale' %(cam[0]))
        mscl = max(max(scl[0][0], scl[0][1]), scl[0][2])
        cmds.spaceLocator(name = '%s_focus' %(cam[0]))
        cmds.setAttr('%s_focus.rotate' %(cam[0]), rot[0][0], rot[0][1], rot[0][2])
        cmds.setAttr('%s_focus.translate' %(cam[0]), pos[0][0], pos[0][1], pos[0][2])
        cmds.setAttr('%s_focus.scale' %(cam[0]), scl[0][0], scl[0][1], scl[0][2])
        cmds.move(0, 0, - mscl, '%s_focus' %(cam[0]), relative = True, objectSpace = True, worldSpaceDistance = True)
        cmds.setAttr('%s.aiEnableDOF' %(obj), 1)
        cmds.expression(string = '%s.aiFocusDistance = sqrt(' %(obj) +\
                                'pow(%s_focus.translateX - %s.translateX, 2) + ' %(cam[0], cam[0]) +\
                                'pow(%s_focus.translateY - %s.translateY, 2) + ' %(cam[0], cam[0]) +\
                                'pow(%s_focus.translateZ - %s.translateZ, 2));' %(cam[0], cam[0]), object = obj)