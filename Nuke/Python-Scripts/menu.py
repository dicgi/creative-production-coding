'''..................................................................................................
Author: Diego Inácio
GitHub: github.com/diegoinacio
..................................................................................................'''
from diNukeScripts import *

#---------------------------------------------------------------------------------------------------------------
# Formats
#---------------------------------------------------------------------------------------------------------------

nuke.addFormat("32 32 0 0 32 32 1.0 square_32")
nuke.addFormat("64 64 0 0 64 64 1.0 square_64")
nuke.addFormat("128 128 0 0 128 128 1.0 square_128")
nuke.addFormat("4096 4096 0 0 4096 4096 1.0 square_4k")

#---------------------------------------------------------------------------------------------------------------
# Defaults
#---------------------------------------------------------------------------------------------------------------

nuke.knobDefault('Write.channels', 'rgba')
nuke.knobDefault('Write.file', '[file dirname [value root.name]]/_RENDER/[lindex [split [file tail [value root.name]] "."] 0]_[knob name]/[lindex [split [file tail [value root.name]] "."] 0]_[knob name].%04d.tiff')
nuke.knobDefault('Write.file_type', 'tiff')

nuke.knobDefault('BlinkScript.kernelSource', 'kernel diBlinkScript: ImageComputationKernel<ePixelWise>{\n\tImage<eRead, eAccessPoint, eEdgeClamped> in;\n\tImage<eWrite> out;\n\n\tparam:\n\t\tfloat mult;\n\n\tlocal:\n\t\tfloat temp;\n\n\tvoid define() {\n\t\tdefineParam(mult, "multiply", 1.0f);\n\t}\n\n\tvoid init() {\n\t\ttemp = 0;\n\t}\n\n\tvoid process() {\n\t\tout() = in() + temp;\n\t}\n};')

#---------------------------------------------------------------------------------------------------------------
# Commands
#---------------------------------------------------------------------------------------------------------------

nuke.menu('Nuke').addCommand('*** diScripts ***/01 - Reload all Read nodes', 'reloadAllReads()')
nuke.menu('Nuke').addCommand('*** diScripts ***/02 - Reload all BlinkScripts', 'reloadAllBlinks()')
nuke.menu('Nuke').addCommand('*** diScripts ***/03 - Open path on explorer', 'pathExplorer()')
nuke.menu('Nuke').addCommand('*** diScripts ***/04 - Create folder from Write nodes', 'writeFolderCreator()')
nuke.menu('Nuke').addCommand('*** diScripts ***/05 - Set multiple knobs', 'setMultipleKnobs()')