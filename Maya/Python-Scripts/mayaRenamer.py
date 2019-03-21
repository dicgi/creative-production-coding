'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: NOV/12/2012
.....................................................................................................
This script is a simple renamer for objects, nodes or anything in your scene do you want to rename.
If you have any comment send it to: diegodci@gmail.com
Thank you! :D
..................................................................................................'''
import maya.cmds as cmds

ui = 'mayaRenamer'
version = '1.0.0'
title = ui + ' ' + version

#############
# Functions #
#############
def closeUI():
    if cmds.window(ui, menuBar = True, exists = True):
        cmds.deleteUI(ui)

def mayaRenamerUI():
    global field1
    global field2
    global field3
    global field4
    global field5
    closeUI()
    cmds.window(ui, title = title, sizeable = False)
    tabs = cmds.tabLayout()
    tab1 = cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 10, columnWidth = 220)
    cmds.separator(style = 'in')
    cmds.text(label = '..: Renamer :..')
    cmds.separator(style = 'out')
    cmds.frameLayout(label = 'Search and Replace', borderStyle='etchedIn', collapse = True, collapsable = True)
    cmds.text(label = 'Search for:')
    field1 = cmds.textField()
    cmds.text(label = 'Replace with:')
    field2 = cmds.textField()
    cmds.button(label = 'Apply', command = 'srOption()')
    cmds.setParent('..')
    cmds.frameLayout(label = 'Prefix and Sufix', borderStyle='etchedIn', collapse = True, collapsable = True)
    cmds.text(label = 'Sufix:')
    field3 = cmds.textField()
    cmds.text(label = 'Prefix:')
    field4 = cmds.textField()
    cmds.button(label = 'Apply', command = 'psOption()')
    cmds.setParent('..')
    cmds.frameLayout(label = 'Rename', borderStyle='etchedIn', collapse = True, collapsable = True)
    cmds.text(label = 'Rename:')
    field5 = cmds.textField()
    cmds.button(label = 'Apply', command = 'rOption()')
    cmds.setParent('..')
    cmds.setParent('..')
    tab2 = cmds.columnLayout(columnAttach = ['both', 5], rowSpacing = 10, columnWidth = 220)
    cmds.text(label = info(), wordWrap = True)
    cmds.tabLayout( tabs, edit=True, tabLabel=((tab1, 'Main'), (tab2, 'Info')))
    cmds.setParent('..')
    cmds.showWindow()

def srOption():
    sel = []
    sel = cmds.ls(selection = True)
    if sel == []: noSelection()
    else:
        search = cmds.textField(field1, text = True, query = True)
        replace = cmds.textField(field2, text = True, query = True)
        for i in range(len(sel)):
            temp = sel[i].replace(search, replace)
            cmds.rename(sel[i], temp)
            
def psOption():
    sel = []
    sel = cmds.ls(selection = True)
    if sel == []: noSelection()
    else:
        prefix = cmds.textField(field3, text = True, query = True)
        sufix = cmds.textField(field4, text = True, query = True)
        for i in range(len(sel)):
            cmds.rename(sel[i], prefix + sel[i] + sufix)

def rOption():
    sel = []
    sel = cmds.ls(selection = True)
    if sel == []: noSelection()
    else:
        renamer = cmds.textField(field5, text = True, query = True)
        for i in range(len(sel)):
            cmds.rename(sel[i], renamer + str(i + 1))

def noSelection():
    cmds.confirmDialog(message = 'no object was selected')

def info():
    infoText = ".: mayaRenamer :.\n\nThis script is a simple renamer for objects, nodes or anything in your scene do you want to rename.\nIf you have any comment, sent it to me at:\ndiegodci@gmail.com\n\nThank you! :D\nDiego Inácio\n"
    return(infoText)

########
# Main #
########
mayaRenamerUI()