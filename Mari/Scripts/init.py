import mari, PythonQt
import sys, os

mari.gl_render.registerCustomHeaderFile('ADJUSTMENT_UTILS_GLSLH', '../Shaders/adjustment/lib/adjUtils.glslh')
mari.gl_render.registerCustomCodeFile('ADJUSTMENT_UTILS_GLSLC', '../Shaders/adjustment/lib/adjUtils.glslc')

mari.gl_render.registerCustomAdjustmentLayerFromXMLFile('Custom-Shaders/Normalize', '%s/Shaders/adjustment/MariNormalize.xml')
mari.gl_render.registerCustomAdjustmentLayerFromXMLFile('Custom-Shaders/Saturation', '%s/Shaders/adjustment/MariSaturation.xml')