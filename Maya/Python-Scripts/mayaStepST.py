'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
.....................................................................................................
If you have any comment send it to: diegodci@gmail.com
Thank you! :D
..................................................................................................'''
import maya.cmds as cmds
import random

script = 'mayaStepST'
version = '1.0.0'
title = script + ' ' + version

def closeUI(scriptUI):
    if cmds.window(scriptUI, menuBar = True, exists = True):
        cmds.deleteUI(scriptUI)

def mayaStepSTUI():
    global cb01, cb02, cb03, tfbg
    closeUI(script)
    cmds.window(script, title = title, widthHeight = (210, 30))
    cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cmds.gridLayout(numberOfColumns = 3, cellWidthHeight = (70, 20))
    cb01 = cmds.checkBox(label = 's', value = True)
    cb02 = cmds.checkBox(label = 't', value = True)
    cb03 = cmds.checkBox(label = 'random', value = False)
    cmds.setParent('..')
    cmds.text(label = '..: steps :..', backgroundColor = [0, 0, 0])
    tfbg = cmds.textFieldButtonGrp(text = '32', buttonLabel = '  ok  ', columnWidth2 = [160, 50], buttonCommand = 'mayaStepST()')
    cmds.setParent('..')
    cmds.showWindow()

def mayaStepST():
    steps = int(cmds.textFieldButtonGrp(tfbg, text = True, query = True))
    cbS = cmds.checkBox(cb01, value = True, query = True)
    cbT = cmds.checkBox(cb02, value = True, query = True)
    cbRandom = cmds.checkBox(cb03, value = True, query = True)
    
    if(cbS):
        s = cmds.shadingNode('ramp', name = 's', asTexture = True)
        
        cmds.setAttr('%s.type' % s, 1)
        cmds.setAttr('%s.interpolation' % s, 0)
        
        if(cbRandom):
            c = random.random()
        else:
            c = 0.0
        p = 0.0
        
        for i in range(steps):
            cmds.setAttr('%s.colorEntryList[%s].color' %(s, i), c, c, c, type = 'double3')
            cmds.setAttr('%s.colorEntryList[%s].position' %(s, i), p)
            
            if(cbRandom):
                c = random.random()
            else:
                c += 1.0/(steps - 1)
            p += 1.0/steps
    
    if(cbT):
        t = cmds.shadingNode('ramp', name = 't', asTexture = True)
        
        cmds.setAttr('%s.type' % t, 0)
        cmds.setAttr('%s.interpolation' % t, 0)
        
        if(cbRandom):
            c = random.random()
        else:
            c = 0.0
        p = 0.0
        
        for i in range(steps):
            cmds.setAttr('%s.colorEntryList[%s].color' %(t, i), c, c, c, type = 'double3')
            cmds.setAttr('%s.colorEntryList[%s].position' %(t, i), p)
            
            if(cbRandom):
                c = random.random()
            else:
                c += 1.0/(steps - 1)
            p += 1.0/steps
    
    closeUI(script)

mayaStepSTUI()