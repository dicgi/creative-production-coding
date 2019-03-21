'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: MAY/28/2015
.....................................................................................................
Arnold attribute manager for maya
If you have any comment send it to: diegodci@gmail.com
Thank you! :D
..................................................................................................'''
import maya.cmds as cmds
import mtoa
import random

script = 'mayaAiAttribManager'
version = '0.9.0 beta'
title = script + ' ' + version

sel = []
texTempList = []
userAttr = ''
dataTypeC = 'float'
dataTypeS = 'float'

def closeUI(scriptUI):
    if cmds.window(scriptUI, menuBar = True, exists = True):
        cmds.deleteUI(scriptUI)
        
def mayaAiAttribManagerUI():
    global cb01, cb02, cb03, cb04, cb05  #checkbox
    global tf01, tf02                    #textField
    global rc01, rc02, rc03              #radioCollection
    global tsl01                         #textScrollList
    closeUI(script)
    cmds.window(script, title = title, sizeable = False)
    tabs = cmds.tabLayout()
    tab01 = cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cmds.separator(style = 'in')
    cmds.text(label = '..: attribute name :..', backgroundColor = [0, 0, 0])
    cmds.separator(style = 'out')
    cmds.gridLayout(numberOfColumns = 2, cellWidthHeight = (105, 20))
    cb01 = cmds.checkBox(label = 'aiAttribute', value = True)
    cb02 = cmds.checkBox(label = 'shapeAttribute', value = True)
    cmds.setParent('..')
    tf01 = cmds.textField()
    cmds.separator(style = 'in')
    cmds.text(label = '..: data type :..', backgroundColor = [0, 0, 0])
    cmds.separator(style = 'out')
    cmds.gridLayout(numberOfColumns = 3, cellWidthHeight = (70, 20))
    rc01 = cmds.radioCollection()
    cmds.radioButton(label = 'float', select = True, onCommand = 'dataTypeC = "float"')
    cmds.radioButton(label = 'integer', onCommand = 'dataTypeC = "long"')
    cmds.radioButton(label = 'boolean', onCommand = 'dataTypeC = "bool"')
    cmds.radioButton(label = 'color', onCommand = 'dataTypeC = "float3"')
    cmds.radioButton(label = 'vector', onCommand = 'dataTypeC = "double3"')
    cmds.radioButton(label = 'string', onCommand = 'dataTypeC = "string"')
    cmds.setParent('..')
    cmds.separator(style = 'out')
    cmds.button(label = 'ok', command = 'createAttribute()')
    cmds.setParent('..')
    tab02 = cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cmds.separator(style = 'in')
    cmds.text(label = '..: attribute :..', backgroundColor = [0, 0, 0])
    cmds.separator(style = 'out')
    cmds.gridLayout(numberOfColumns = 2, cellWidthHeight = (105, 20))
    cb03 = cmds.checkBox(label = 'aiAttribute', value = True)
    cb04 = cmds.checkBox(label = 'shapeAttribute', value = True)
    cmds.setParent('..')
    tf02 = cmds.textField()
    cmds.separator(style = 'in')
    cmds.text(label = '..: type :..', backgroundColor = [0, 0, 0])
    cmds.separator(style = 'out')
    cmds.gridLayout(numberOfColumns = 3, cellWidthHeight = (70, 20))
    rc03 = cmds.radioCollection()
    cmds.radioButton(label = 'float', select = True, onCommand = 'dataTypeS = "float"')
    cmds.radioButton(label = 'integer', onCommand = 'dataTypeS = "long"')
    cmds.radioButton(label = 'boolean', onCommand = 'dataTypeS = "bool"')
    cmds.radioButton(label = 'color', onCommand = 'dataTypeS = "float3"')
    cmds.radioButton(label = 'vector', onCommand = 'dataTypeS = "double3"')
    cmds.radioButton(label = 'string', onCommand = 'dataTypeS = "string"')
    cmds.setParent('..')
    cmds.separator(style = 'out')
    cmds.button(label = 'set/edit', command = 'setAttribute()')
    cmds.setParent('..')
    tab03 = cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cb05 = cmds.checkBox(label = 'shapeAttribute', value = True)
    tsl01 = cmds.textScrollList(allowMultiSelection = True)
    cmds.button('scan', command = 'scan()')
    cmds.button('delete', command = 'delete()')
    cmds.setParent('..')
    cmds.tabLayout(tabs, edit=True, tabLabel=((tab01, 'create'), (tab02, 'set/edit'), (tab03, 'delete')))
    cmds.showWindow()

def createAttribute():
    if(not cmds.textField(tf01, text = True, query = True) == ''):
        niceName, longName = attrNameDefC()
        sel = selectListC()
        if(dataTypeC == 'float3'):
            for obj in sel:
                if(not cmds.attributeQuery(longName, node = obj, exists = True)):
                    cmds.addAttr(obj, niceName = niceName, longName = longName, usedAsColor = True, attributeType = dataTypeC)
                    cmds.addAttr(obj, longName = '%sR' % longName, attributeType = 'float', parent = longName)
                    cmds.addAttr(obj, longName = '%sG' % longName, attributeType = 'float', parent = longName)
                    cmds.addAttr(obj, longName = '%sB' % longName, attributeType = 'float', parent = longName)
        elif(dataTypeC == 'double3'):
            for obj in sel:
                if(not cmds.attributeQuery(longName, node = obj, exists = True)):
                    cmds.addAttr(obj, niceName = niceName, longName = longName, attributeType = dataTypeC)
                    cmds.addAttr(obj, longName = '%sX' % longName, attributeType = 'double', parent = longName)
                    cmds.addAttr(obj, longName = '%sY' % longName, attributeType = 'double', parent = longName)
                    cmds.addAttr(obj, longName = '%sZ' % longName, attributeType = 'double', parent = longName)
        elif(dataTypeC == 'string'):
            for obj in sel:
                if(not cmds.attributeQuery(longName, node = obj, exists = True)):
                    cmds.addAttr(obj, niceName = niceName, longName = longName, dataType = dataTypeC)
        else:
            for obj in sel:
                if(not cmds.attributeQuery(longName, node = obj, exists = True)):
                    cmds.addAttr(obj, niceName = niceName, longName = longName, attributeType = dataTypeC)
        cmds.textField(tf01, text = '', edit = True)

def setAttribute():
    if(dataTypeS == 'float'):
        setAttributeFloatUI()
    if(dataTypeS == 'long'):
        setAttributeIntUI()
    if(dataTypeS == 'bool'):
        setAttributeBoolUI()
    if(dataTypeS == 'float3'):
        setAttributeColorUI()
    if(dataTypeS == 'double3'):
        setAttributeVectorUI()
    if(dataTypeS == 'string'):
        setAttributeStringUI()

def setAttributeFloatUI():
    global tfInF, tfOutF, tfStepF, floatUI
    floatUI = 'floatUI'
    closeUI(floatUI)
    cmds.window(floatUI, title = 'floatUI')
    cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cmds.separator(style = 'in')
    cmds.text(label = '..: random range :..', backgroundColor = [0.15, 0.1, 0])
    cmds.separator(style = 'out')
    cmds.gridLayout(numberOfColumns = 2, cellWidthHeight = (100, 20))
    tfInF = cmds.textField(text = '0.0')
    tfOutF = cmds.textField(text = '1.0')
    cmds.setParent('..')
    cmds.button(label = 'ok', command = 'setAttributeFloatRandom()')
    cmds.separator(style = 'in')
    cmds.text(label = '..: increment step :..', backgroundColor = [0, 0.1, 0.15])
    cmds.separator(style = 'out')
    tfStepF = cmds.textField(text = '0.1')
    cmds.separator(style = 'out')
    cmds.button(label = 'ok', command = 'setAttributeFloatIncrement()')
    cmds.setParent('..')
    cmds.showWindow()

def setAttributeFloatRandom():
    userAttr = attrNameDefS()
    sel = selectListS()
    rIn = float(cmds.textField(tfInF, text = True, query = True))
    rOut = float(cmds.textField(tfOutF, text = True, query = True))
    for obj in sel:
        type = cmds.attributeQuery(userAttr, node = obj, attributeType = True)
        if(not type == dataTypeS):
            continue
        try:
            rand = rIn + random.random()*(rOut - rIn)
            cmds.setAttr('%s.%s' %(obj, userAttr), rand)
        except:
            continue
    closeUI(floatUI)

def setAttributeFloatIncrement():
    userAttr = attrNameDefS()
    sel = selectList()
    rStep = float(cmds.textField(tfStepF, text = True, query = True))
    step = 0.0
    for obj in sel:
        type = cmds.attributeQuery(userAttr, node = obj, attributeType = True)
        if(not type == dataTypeS):
            continue
        try:
            cmds.setAttr('%s.%s' %(obj, userAttr), step)
            step += rStep
        except:
            continue
    closeUI(floatUI)

def setAttributeIntUI():
    global tfInI, tfOutI, tfStepI, intUI
    intUI = 'intUI'
    closeUI(intUI)
    cmds.window(intUI, title = 'intUI')
    cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cmds.separator(style = 'in')
    cmds.text(label = '..: random range :..', backgroundColor = [0.15, 0.1, 0])
    cmds.separator(style = 'out')
    cmds.gridLayout(numberOfColumns = 2, cellWidthHeight = (100, 20))
    tfInI = cmds.textField(text = '0')
    tfOutI = cmds.textField(text = '4')
    cmds.setParent('..')
    cmds.button(label = 'ok', command = 'setAttributeIntRandom()')
    cmds.separator(style = 'in')
    cmds.text(label = '..: increment step :..', backgroundColor = [0, 0.1, 0.15])
    cmds.separator(style = 'out')
    tfStepI = cmds.textField(text = '1')
    cmds.separator(style = 'out')
    cmds.button(label = 'ok', command = 'setAttributeIntIncrement()')
    cmds.setParent('..')
    cmds.showWindow()

def setAttributeIntRandom():
    userAttr = attrNameDefS()
    sel = selectList()
    rIn = int(cmds.textField(tfInI, text = True, query = True))
    rOut = int(cmds.textField(tfOutI, text = True, query = True))
    for obj in sel:
        type = cmds.attributeQuery(userAttr, node = obj, attributeType = True)
        if(not type == dataTypeS):
            continue
        try:
            rand = rIn + random.random()*(rOut - rIn)
            cmds.setAttr('%s.%s' %(obj, userAttr), rand)
        except:
            continue
    closeUI(intUI)

def setAttributeIntIncrement():
    userAttr = attrNameDefS()
    sel = selectList()
    rStep = int(cmds.textField(tfStepI, text = True, query = True))
    step = 0
    print dataTypeC
    for obj in sel:
        type = cmds.attributeQuery(userAttr, node = obj, attributeType = True)
        if(not type == dataTypeS):
            continue
        try:
            cmds.setAttr('%s.%s' %(obj, userAttr), step)
            step += rStep
        except:
            continue
    closeUI(intUI)

def setAttributeBoolUI():
    global boolUI
    boolUI = 'boolUI'
    closeUI(boolUI)
    cmds.window(boolUI, title = 'boolUI')
    cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cmds.separator(style = 'in')
    cmds.text(label = '..: random :..', backgroundColor = [0.15, 0.1, 0])
    cmds.separator(style = 'out')
    cmds.button(label = 'ok', command = 'setAttributeBoolRandom()')
    cmds.setParent('..')
    cmds.showWindow()

def setAttributeBoolRandom():
    userAttr = attrNameDefS()
    sel = selectList()
    for obj in sel:
        type = cmds.attributeQuery(userAttr, node = obj, attributeType = True)
        if(not type == dataTypeS):
            continue
        try:
            rand = random.random()
            if(rand <= 0.5):
                cmds.setAttr('%s.%s' %(obj, userAttr), True)
            else:
                cmds.setAttr('%s.%s' %(obj, userAttr), False)
        except:
            continue
    closeUI(boolUI)

def setAttributeColorUI():
    global csbgColor, tslColorList, colorUI
    colorUI = 'colorUI'
    closeUI(colorUI)
    cmds.window(colorUI, title = 'colorUI')
    cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cmds.text('..: random color :..', backgroundColor = (0.15, 0.15, 0.0))
    cmds.button('ok', command = 'setAttributeColorRandom()')
    cmds.separator(style = 'out')
    cmds.text('..: color list :..', backgroundColor = (0.0, 0.15, 0.15))
    tslColorList = cmds.textScrollList(allowMultiSelection = True)
    cmds.button('remove', command = 'removeScrollListColor()')
    csbgColor = cmds.colorSliderButtonGrp(buttonLabel='add..', 
                                            symbolButtonDisplay=True, 
                                            image='navButtonUnconnected.png', 
                                            columnWidth4 = [30, 100, 30, 50],
                                            buttonCommand = 'addScrollListColor()',
                                            symbolButtonCommand = 'addScrollListTex()')
    cmds.button('random', command = 'setAttributeListColorRandom()')
    cmds.button('increment %', command = 'setAttributeListColorInc()')
    cmds.setParent('..')
    cmds.showWindow()

def setAttributeColorRandom():
    userAttr = attrNameDefS()
    sel = selectListS()
    for obj in sel:
        try:
            type = cmds.attributeQuery(userAttr, node = obj, attributeType = True)
        except:
            continue
        if(not type == dataTypeS):
            continue
        try:
            randR = random.random()
            randG = random.random()
            randB = random.random()
            cmds.setAttr('%s.%s' %(obj, userAttr), randR, randG, randB)
        except:
            continue
    closeUI(colorUI)

def scrollListItemsColor():
    try:
        return list(cmds.textScrollList(tslColorList, allItems = True, query = True))
    except:
        return []

def removeScrollListColor():
    tsList = scrollListItemsColor()
    selectedItems = cmds.textScrollList(tslColorList, selectItem = True, query = True)
    if(not selectedItems == None):
        for item in selectedItems:
            tsList.remove(item)
        cmds.textScrollList(tslColorList, edit = True, removeAll = True)
        cmds.textScrollList(tslColorList, edit = True, append = tsList)

def addScrollListColor():
    tsList = scrollListItemsColor()
    cAdd = cmds.colorSliderButtonGrp(csbgColor, rgbValue = True, query = True)
    tsList.append('%s, %s, %s' %(cAdd[0], cAdd[1], cAdd[2]))
    cmds.textScrollList(tslColorList, edit = True, removeAll = True)
    cmds.textScrollList(tslColorList, append = tsList, edit = True)
    cmds.colorSliderButtonGrp(csbgColor, rgbValue = [1.0, 1.0, 1.0], edit = True)

def addScrollListTex():
    sel = selectListS()
    texTemp = cmds.group(name = 'texTempNode', empty = True)
    texTempList.append(texTemp)
    cmds.addAttr(texTemp, longName = 'texTemp', usedAsColor = True, attributeType = 'float3')
    cmds.addAttr(longName = 'texTempR', attributeType = 'float', parent = 'texTemp')
    cmds.addAttr(longName = 'texTempG', attributeType = 'float', parent = 'texTemp')
    cmds.addAttr(longName = 'texTempB', attributeType = 'float', parent = 'texTemp')
    cmds.defaultNavigation(createNew = True, destination = '%s.texTemp' % texTemp)
    tsList = scrollListItemsColor()
    tsList.append(texTemp)
    cmds.textScrollList(tslColorList, edit = True, removeAll = True)
    cmds.textScrollList(tslColorList, append = tsList, edit = True)

def setAttributeListColorRandom():
    tsList = scrollListItemsColor()
    userAttr = attrNameDefS()
    sel = selectListS()
    if(not (tsList == None or tsList == [])):
        for obj in sel:
            index = int(random.random()*len(tsList))
            if(len(tsList[index].split(',')) == 3):
                r, g, b = tsList[index].split(',')
                cmds.setAttr('%s.%s' %(obj, userAttr), float(r), float(g), float(b))
            else:
                texIn = cmds.connectionInfo('%s.texTemp' % tsList[index], sourceFromDestination = True)
                cmds.connectAttr(texIn, '%s.%s' %(obj, userAttr), force = True)
        else:
            eraseTexTempList()
    closeUI(colorUI)

def setAttributeListColorInc():
    tsList = scrollListItemsColor()
    userAttr = attrNameDefS()
    sel = selectListS()
    if(not (tsList == None or tsList == [])):
        for i in range(len(tsList)):
            index = i % len(tsList)
            if(len(tsList[index].split(',')) == 3):
                r, g, b = tsList[index].split(',')
                cmds.setAttr('%s.%s' %(sel[i], userAttr), float(r), float(g), float(b))
            else:
                texIn = cmds.connectionInfo('%s.texTemp' % tsList[index], sourceFromDestination = True)
                cmds.connectAttr(texIn, '%s.%s' %(sel[i], userAttr), force = True)
        else:
            eraseTexTempList()
    closeUI(colorUI)

def eraseTexTempList():
    for i in range(len(texTempList)):
        cmds.delete(texTempList[i])

def setAttributeVectorUI():
    global tfXIn, tfXOut, tfYIn, tfYOut, tfZIn, tfZOut, tslVectorList, tfXAdd, tfYAdd, tfZAdd, vectorUI
    vectorUI = 'vectorUI'
    closeUI(vectorUI)
    cmds.window(vectorUI, title = 'vectorUI')
    cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    cmds.text('..: random range :..', backgroundColor = [0.15, 0.15, 0.0])
    cmds.gridLayout(numberOfColumns = 6, cellWidthHeight = (33, 20))
    tfXIn = cmds.textField(text = '0.0', backgroundColor = [0.15, 0.1, 0.0])
    tfXOut = cmds.textField(text = '1.0', backgroundColor = [0.15, 0.1, 0.0])
    tfYIn = cmds.textField(text = '0.0', backgroundColor = [0.0, 0.15, 0.1])
    tfYOut = cmds.textField(text = '1.0', backgroundColor = [0.0, 0.15, 0.1])
    tfZIn = cmds.textField(text = '0.0', backgroundColor = [0.0, 0.1, 0.15])
    tfZOut = cmds.textField(text = '1.0', backgroundColor = [0.0, 0.1, 0.15])
    cmds.setParent('..')
    cmds.button('ok', command = 'setAttributeVectorRandom()')
    cmds.separator(style = 'out')
    cmds.text('..: vector list :..', backgroundColor = [0.0, 0.15, 0.15])
    tslVectorList = cmds.textScrollList(allowMultiSelection = True)
    cmds.button('remove', command = 'removeScrollListVector()')
    cmds.gridLayout(numberOfColumns = 4, cellWidthHeight = (50, 20))
    tfXAdd = cmds.textField(text = '0.0', backgroundColor = [0.15, 0.1, 0.0])
    tfYAdd = cmds.textField(text = '0.0', backgroundColor = [0.0, 0.15, 0.1])
    tfZAdd = cmds.textField(text = '0.0', backgroundColor = [0.0, 0.1, 0.15])
    cmds.button('add..', command = 'addScrollListVector()')
    cmds.setParent('..')
    cmds.button('random', command = 'setAttributeListVectorRandom()')
    cmds.button('increment %', command = 'setAttributeListVectorInc()')
    cmds.setParent('..')
    cmds.showWindow()

def setAttributeVectorRandom():
    userAttr = attrNameDefS()
    sel = selectListS()
    xIn = float(cmds.textField(tfXIn, text = True, query = True))
    xOut = float(cmds.textField(tfXOut, text = True, query = True))
    yIn = float(cmds.textField(tfYIn, text = True, query = True))
    yOut = float(cmds.textField(tfYOut, text = True, query = True))
    zIn = float(cmds.textField(tfZIn, text = True, query = True))
    zOut = float(cmds.textField(tfZOut, text = True, query = True))
    for obj in sel:
        try:
            type = cmds.attributeQuery(userAttr, node = obj, attributeType = True)
        except:
            continue
        if(not type == dataTypeS):
            continue
        try:
            randX = xIn + random.random()*(xOut - xIn)
            randY = yIn + random.random()*(yOut - yIn)
            randZ = zIn + random.random()*(zOut - zIn)
            cmds.setAttr('%s.%s' %(obj, userAttr), randX, randY, randZ)
        except:
            continue
    closeUI(vectorUI)

def scrollListItemsVector():
    try:
        return list(cmds.textScrollList(tslVectorList, allItems = True, query = True))
    except:
        return []

def removeScrollListVector():
    tsList = scrollListItemsVector()
    selectedItems = cmds.textScrollList(tslVectorList, selectItem = True, query = True)
    if(not selectedItems == None):
        for item in selectedItems:
            tsList.remove(item)
        cmds.textScrollList(tslVectorList, edit = True, removeAll = True)
        cmds.textScrollList(tslVectorList, edit = True, append = tsList)

def addScrollListVector():
    tsList = scrollListItemsVector()
    x = cmds.textField(tfXAdd, text = True, query = True)
    y = cmds.textField(tfYAdd, text = True, query = True)
    z = cmds.textField(tfZAdd, text = True, query = True)
    tsList.append('%s, %s, %s' %(float(x), float(y), float(z)))
    cmds.textScrollList(tslVectorList, edit = True, removeAll = True)
    cmds.textScrollList(tslVectorList, append = tsList, edit = True)
    cmds.textField(tfXAdd, text = '0.0', edit = True)
    cmds.textField(tfYAdd, text = '0.0', edit = True)
    cmds.textField(tfZAdd, text = '0.0', edit = True)

def setAttributeListVectorRandom():
    tsList = scrollListItemsVector()
    userAttr = attrNameDefS()
    sel = selectListS()
    if(not (tsList == None or tsList == [])):
        for obj in sel:
            index = int(random.random()*len(tsList))
            x, y, z = tsList[index].split(',')
            cmds.setAttr('%s.%s' %(obj, userAttr), float(x), float(y), float(z))

def setAttributeListVectorInc():
    tsList = scrollListItemsVector()
    userAttr = attrNameDefS()
    sel = selectListS()
    if(not (tsList == None or tsList == [])):
        for i in range(len(sel)):
            index = i % len(tsList)
            x, y, z = tsList[index].split(',')
            cmds.setAttr('%s.%s' %(sel[i], userAttr), float(x), float(y), float(z))

def setAttributeStringUI():
    global tslStringList, tfbgAdd, stringUI
    stringUI = 'stringUI'
    closeUI(stringUI)
    cmds.window(stringUI, title = 'stringUI')
    cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 5, columnWidth = 210)
    tslStringList = cmds.textScrollList(allowMultiSelection = True)
    cmds.button('remove', command = 'removeScrollListString()')
    tfbgAdd = cmds.textFieldButtonGrp(buttonLabel = 'add..', 
                                        columnWidth2 = [160, 50], 
                                        buttonCommand = 'addScrollListString()')
    cmds.separator(style = 'out')
    cmds.button('random', command = 'setAttributeStringRandom()')
    cmds.button('increment %', command = 'setAttributeStringInc()')
    cmds.setParent('..')
    cmds.showWindow()

def scrollListItemsString():
    try:
        return list(cmds.textScrollList(tslStringList, allItems = True, query = True))
    except:
        return []

def removeScrollListString():
    tsList = scrollListItemsString()
    selectedItems = cmds.textScrollList(tslStringList, selectItem = True, query = True)
    if(not selectedItems == None):
        for item in selectedItems:
            tsList.remove(item)
        cmds.textScrollList(tslStringList, edit = True, removeAll = True)
        cmds.textScrollList(tslStringList, edit = True, append = tsList)

def addScrollListString():
    tsList = scrollListItemsString()
    addList = cmds.textFieldButtonGrp(tfbgAdd, text = True, query = True).split(',')
    for item in addList:
        if(not item == ''):
            tsList.append(item.strip())
    cmds.textScrollList(tslStringList, edit = True, removeAll = True)
    cmds.textScrollList(tslStringList, append = tsList, edit = True)
    cmds.textFieldButtonGrp(tfbgAdd, edit = True, text = '')

def setAttributeStringRandom():
    tsList = scrollListItemsString()
    userAttr = attrNameDefS()
    sel = selectListS()
    if(not (tsList == None or tsList == [])):
        for obj in sel:
            index = int(random.random()*len(tsList))
            cmds.setAttr('%s.%s' %(obj, userAttr), tsList[index], type = 'string')

def setAttributeStringInc():
    tsList = scrollListItemsString()
    userAttr = attrNameDefS()
    sel = selectListS()
    if(not (tsList == None or tsList == [])):
        for i in range(len(sel)):
            index = i % len(tsList)
            cmds.setAttr('%s.%s' %(sel[i], userAttr), tsList[index], type = 'string')

def scan():
    scanList = []
    cmds.textScrollList(tsl01, edit = True, removeAll = True)
    if(cmds.checkBox(cb05, value = True, query = True)):
        sel = cmds.ls(selection = True, dagObjects = True, leaf = True)
    else:
        sel = cmds.ls(selection = True, allPaths = True, dagObjects = True)
    for obj in sel:
        attrList = cmds.listAttr(obj, userDefined = True)
        if(not attrList == None):
            for attr in attrList:
                try:
                    scanList.remove(attr)
                    scanList.append(attr)
                except:
                    scanList.append(attr)
    cmds.textScrollList(tsl01, edit = True, append = scanList)

def delete():
    if(cmds.checkBox(cb05, value = True, query = True)):
        sel = cmds.ls(selection = True, dagObjects = True, leaf = True)
    else:
        sel = cmds.ls(selection = True, allPaths = True, dagObjects = True)
    selectedAttr = cmds.textScrollList(tsl01, selectItem = True, query = True)
    if(not selectedAttr == None):
        for obj in sel:
            for attr in selectedAttr:
                try:
                    cmds.deleteAttr(obj, attribute = attr)
                except:
                    continue
    scan()

def attrNameDefC():
    if(cmds.checkBox(cb01, value = True, query = True)):
        return 'ai ' + cmds.textField(tf01, text = True, query = True), 'mtoa_constant_' + cmds.textField(tf01, text = True, query = True)
    else:
        return cmds.textField(tf01, text = True, query = True), cmds.textField(tf01, text = True, query = True)

def selectListC():
    if(cmds.checkBox(cb02, value = True, query = True)):
        return cmds.ls(selection = True, dagObjects = True, leaf = True)
    else:
        return cmds.ls(selection = True, allPaths = True, dagObjects = True)

def attrNameDefS():
    if(cmds.checkBox(cb03, value = True, query = True)):
        return 'mtoa_constant_' + cmds.textField(tf02, text = True, query = True)
    else:
        return cmds.textField(tf02, text = True, query = True)

def selectListS():
    if(cmds.checkBox(cb04, value = True, query = True)):
        return cmds.ls(selection = True, dagObjects = True, leaf = True)
    else:
        return cmds.ls(selection = True, allPaths = True, dagObjects = True)

mayaAiAttribManagerUI()