'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: SEP/01/2016
..................................................................................................'''
import nuke

def reloadAllReads():
	'''
	Reload all read nodes
	'''
	nodes = [node for node in nuke.allNodes(recurseGroups = True) if node.Class() == 'Read']
	for node in nodes:
		node.knob('reload').execute()

def reloadAllBlinks():
	'''
	Reload all blinkScript nodes
	'''
	nodes = [node for node in nuke.allNodes(recurseGroups = True) if node.Class() == 'BlinkScript']
	for node in nodes:
		nuke.show(node)
		node.knob('reloadKernelSourceFile').execute()
		node.hideControlPanel()

def pathExplorer():
	'''
	Open filename's path on explorer from Read or Write selected nodes
	'''
	import os, subprocess
	
	sel = nuke.selectedNodes()
	for node in sel:
		if node.Class() == 'Read' or node.Class() == 'Write':
			File = nuke.filename(node)
			path = os.path.dirname(File)
			subprocess.Popen('explorer "%s"' % path.replace('/', '\\'))

def writeFolderCreator():
	'''
	Checks if selected write node's folder exists and create them if does not
	'''
	import os
	
	nodes = nuke.selectedNodes('Write')
	if nodes == []:
		nuke.message('select some write node')
		return None
	
	for node in nodes:
		file = nuke.filename(node)
		path = os.path.dirname(file)
		if not os.path.isdir(path):
			if nuke.ask(node.knob('name').getValue() + '\n\n' + path +\
						'\n\nthis path does not exist. would like to create it?'):
				os.makedirs(path)

def setMultipleKnobs():
	'''
	Set multiple knobs into multiple selected nodes
	'''
	import ast
	
	nodes = nuke.selectedNodes()
	if nodes == []:
		nuke.message('select some node')
		return None
	
	classes = set()
	for node in nodes:
		classes.add(node.Class())
	enumClasses = ' '.join(['all'] + list(classes))

	p = nuke.Panel('set multiple knobs')
	p.addEnumerationPulldown('node class', enumClasses)
	p.addSingleLineInput('knob name', '')
	p.addSingleLineInput('value', '')
	c = p.show()

	if c:
		nodeClass = p.value('node class')
		knobName = [e.lstrip() for e in p.value('knob name').split(',')]
		try:
			value = list(ast.literal_eval(p.value('value')))
		except:
			value = [eval(p.value('value'))]

		if len(knobName) != len(value):
			nuke.message(	"the knobName's field and the value's \
							field must have the same number of arguments")
			return None

		for node in nodes:
			if node.Class() == nodeClass or nodeClass == 'all':
				for index in range(len(knobName)):
					node.knob(knobName[index]).setValue(value[index])