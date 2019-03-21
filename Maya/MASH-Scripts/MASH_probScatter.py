'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
  Date: AUG/28/2018
.....................................................................................................
Script do tipo "Drop Window" para para scatter de instancias sobre uma superficie.
- Suporte para probabilidade e controle de ID por meio de pesos. (node Python)
- Numero instancias devem ser maior ou igual a 2. Superficie deve ser apenas uma.
- Variacoes de escala, rotacao e etc. (node Random)
- Controle de densidade e escala. (node Strength)
..................................................................................................'''
import MASH.api as mapi
import flux.core as fx
import maya.cmds as cmds

SCRIPT = '''# script para randomizacao por meio de probabilidade
import openMASH
import random

# inicializacao do sistema MASH
md = openMASH.MASHData(thisNode)
count = md.count()

# recebe valores dos atributos do node python
countID = cmds.getAttr(thisNode + '.countID')
seed = cmds.getAttr(thisNode + '.seed')

##############
# parametros #
##############
random.seed(seed)
# numero de ids
ids = countID
# lista de pesos
p = [1]*ids

# set de probabilidade
{0}
# calculo de probabilidade
p = [float(e)/sum(p) for e in p]
p = [int(e*count + 0.5) for e in p]
if sum(p) != count:
	diff = count - sum(p)
	argmax = p.index(max(p))
	p[argmax] += diff
ID = sum([[i]*p[i] for i in range(ids)], [])
random.shuffle(ID)

for i in range(count):
	md.outId[i] = ID[i]

md.setData()
'''

def runPreset():
	cmds.select(clear=True)
	cmds.promptDialog(message='Nome do sistema MASH:')
	mashName = cmds.promptDialog(query=True, text=True)
	if not mashName:
		mashName = '#'
	else:
		mashName = '_' + mashName
	############################################################################################
	steps = [	'Selecione as instancias | n >= 2 (arraste com o botao do meio)',
				'Selecione a superficie  | n = 1  (arraste com o botao do meio)']
	accepts = [['mesh'], ['mesh']]
	############################################################################################
	fx.DropWindow.getDrop(	steps,
							lambda data: smartPreset.send(data),
							accepts=accepts)
	node = yield
	nodes = node.split('\n')
	############################################################################################
	cmds.promptDialog(message='Numero de pontos:')
	pointCount = cmds.promptDialog(query=True, text=True)
	try:
		pointCount =  int(pointCount)
	except:
		pointCount = 10
	
	mash = mapi.Network()
	mash.createNetwork(name='MASH' + mashName, geometry='Instancer')

	node = yield
	node = node.split('\n')[0]

	mash.meshDistribute(node)
	############################################################################################
	distNodeName = mash.waiter + '_Distribute'
	cmds.setAttr(distNodeName + '.pointCount', pointCount)

	idNodeName = mash.waiter + '_ID'
	cmds.setAttr(idNodeName + '.idtype', 2)
	count = cmds.getAttr(idNodeName + '.numObjects')

	pyNode = mash.addNode('MASH_Python')
	cmds.addAttr(pyNode.name, longName='countID', attributeType='long', defaultValue=count)
	expr = '{0}.countID = {1}.numObjects'.format(pyNode.name, idNodeName)
	cmds.expression(s=expr)
	cmds.addAttr(pyNode.name, longName='seed', attributeType='long', defaultValue=1234)
	scriptID = ''.join(['p[{0}] = 1  # {1} prob.\n'.format(i, e) for i, e in enumerate(nodes)])
	cmds.setAttr(pyNode.name + '.pyScript', SCRIPT.format(scriptID), type='string')

	randNode = mash.addNode('MASH_Random')
	cmds.setAttr(randNode.name + '.positionX', 0)
	cmds.setAttr(randNode.name + '.positionY', 0)
	cmds.setAttr(randNode.name + '.positionZ', 0)
	cmds.setAttr(randNode.name + '.rotationY', 180)
	cmds.setAttr(randNode.name + '.scaleX', 1)
	cmds.setAttr(randNode.name + '.uniformRandom', 1)

	strengthNode = mash.addNode('MASH_Strength')

	yield

smartPreset = runPreset()
smartPreset.next()