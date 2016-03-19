bl_info = {
	"name": "AutoSnap",
	"author": "Julien Duroure",
	"version": (0, 0, 1),
	"blender": (2,77, 0),
	"description": "Add snapping FK/IK automatically",
	"location": "View 3D tools, tab 'AutoSnap'",
	"wiki_url": "http://julienduroure.com/AutoSnap",
	"tracker_url": "https://github.com/julienduroure/AutoSnap",
	"category": "Rigging",   
}

if "bpy" in locals():
	import imp
	imp.reload(addon_prefs)
	imp.reload(ui_texts)
	imp.reload(globals)
	imp.reload(utils)
	imp.reload(ui)
	imp.reload(ui_ops)
	imp.reload(ops)
else:
	from .addon_prefs import *
	from .ui_texts import *
	from .globals import *
	from .utils import *
	from . import ui
	from . import ui_ops
	from . import ops

import bpy

def register():
	addon_prefs.register()
	globals.register()
	ops.register()
	ui_ops.register()
	ui.register()
	
	bpy.types.Object.generation = bpy.props.PointerProperty(type=AutoSnap_Generation)
	bpy.types.Object.limbs = bpy.props.CollectionProperty(type=LimbItem)
	bpy.types.Object.active_limb = bpy.props.IntProperty()
	
	bpy.types.Scene.sides = bpy.props.CollectionProperty(type=SideItem) #ADDON : move to addon pref
	bpy.types.Scene.active_side = bpy.props.IntProperty()               #ADDON : move to addon pref
	
def unregister():
	addon_prefs.unregister()
	globals.unregister()
	ops.unregister()
	ui_ops.unregister()
	ui.unregister()

	del bpy.types.Object.generation
	del bpy.types.Object.limbs
	del bpy.types.Object.active_limb
	
	del bpy.types.Scene.sides       #ADDON move to addon pref
	del bpy.types.Scene.active_side #ADDON move to addon pref
	

if __name__ == "__main__":
	register()
