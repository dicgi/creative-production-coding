'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: OCT/28/2014
.....................................................................................................
This script creates three RGB aiUtilities.
If you have any comment send it to: diegodci@gmail.com
Thank you! :D
..................................................................................................'''
import maya.cmds as cmds
import mtoa

script = 'mayaAiIDshader'
version = '1.0.0'
title = script + ' ' + version

def closeUI(scriptUI):
    if cmds.window(scriptUI, menuBar = True, exists = True):
        cmds.deleteUI(scriptUI)

def mayaAiIDshaderUI():
    global cb01, cb02, cb03, cb04, cb05, cb06  #checkbox
    closeUI(script)
    cmds.window(script, title = title, sizeable = False)
    cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 315)
    cmds.separator(style = 'in')
    cmds.text(label = '..: id shader :..', backgroundColor = [0, 0, 0])
    cmds.separator(style = 'out')
    cmds.gridLayout(numberOfColumns = 3, cellWidthHeight = (105, 20))
    cb01 = cmds.checkBox(label = 'red', value = True)
    cb02 = cmds.checkBox(label = 'green', value = True)
    cb03 = cmds.checkBox(label = 'blue', value = True)
    cb04 = cmds.checkBox(label = 'black', value = False)
    cb05 = cmds.checkBox(label = 'white', value = False)
    cb06 = cmds.checkBox(label = 'black hole', value = False)
    cmds.setParent('..')
    cmds.button('ok', command = 'mayaAiIDshader()')
    cmds.showWindow()

def mayaAiIDshader():
    if(cmds.checkBox(cb01, value = True, query = True)):
        if(not cmds.objExists('aiIDRed')):
            mtoa.core.createArnoldNode('aiUtility', name = 'aiIDRed')
            cmds.setAttr('aiIDRed.shadeMode', 2)
            cmds.setAttr('aiIDRed.color', 1, 0, 0, type = 'double3')
            cmds.setAttr('aiIDRed.hardwareColor', 1, 0, 0, type = 'double3')
        
    if(cmds.checkBox(cb02, value = True, query = True)):
        if(not cmds.objExists('aiIDGreen')):
            mtoa.core.createArnoldNode('aiUtility', name = 'aiIDGreen')
            cmds.setAttr('aiIDGreen.shadeMode', 2)
            cmds.setAttr('aiIDGreen.color', 0, 1, 0, type = 'double3')
            cmds.setAttr('aiIDGreen.hardwareColor', 0, 1, 0, type = 'double3')
    
    if(cmds.checkBox(cb03, value = True, query = True)):
        if(not cmds.objExists('aiIDBlue')):
            mtoa.core.createArnoldNode('aiUtility', name = 'aiIDBlue')
            cmds.setAttr('aiIDBlue.shadeMode', 2)
            cmds.setAttr('aiIDBlue.color', 0, 0, 1, type = 'double3')
            cmds.setAttr('aiIDBlue.hardwareColor', 0, 0, 1, type = 'double3')

    if(cmds.checkBox(cb04, value = True, query = True)):
        if(not cmds.objExists('aiIDBlack')):
            mtoa.core.createArnoldNode('aiUtility', name = 'aiIDBlack')
            cmds.setAttr('aiIDBlack.shadeMode', 2)
            cmds.setAttr('aiIDBlack.color', 0, 0, 0, type = 'double3')
            cmds.setAttr('aiIDBlack.hardwareColor', 0, 0, 0, type = 'double3')
        
    if(cmds.checkBox(cb05, value = True, query = True)):
        if(not cmds.objExists('aiIDWhite')):
            mtoa.core.createArnoldNode('aiUtility', name = 'aiIDWhite')
            cmds.setAttr('aiIDWhite.shadeMode', 2)
            cmds.setAttr('aiIDWhite.color', 1, 1, 1, type = 'double3')
            cmds.setAttr('aiIDWhite.hardwareColor', 1, 1, 1, type = 'double3')
    
    if(cmds.checkBox(cb06, value = True, query = True)):
        if(not cmds.objExists('aiBlackHole')):
            mtoa.core.createArnoldNode('aiStandard', name = 'aiBlackHole')
            cmds.setAttr('aiBlackHole.aiEnableMatte', 1)
            cmds.setAttr('aiBlackHole.color', 0.01, 0.01, 0.01, type = 'double3')

mayaAiIDshaderUI()