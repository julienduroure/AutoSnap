##########################################################################################
#	GPL LICENSE:
#-------------------------
# This file is part of AutoSnap.
#
#    AutoSnap is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AutoSnap is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AutoSnap.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################################
#
#	Copyright 2016 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################

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
	"warning": "Alpha Version. Please report bugs :)",
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
	
	bpy.types.Object.juas_generation = bpy.props.PointerProperty(type=JuAS_Generation)
	bpy.types.Object.juas_limbs = bpy.props.CollectionProperty(type=JuAS_LimbItem)
	bpy.types.Object.juas_active_limb = bpy.props.IntProperty()
	
	
def unregister():
	addon_prefs.unregister()
	globals.unregister()
	ops.unregister()
	ui_ops.unregister()
	ui.unregister()

	del bpy.types.Object.juas_generation
	del bpy.types.Object.juas_limbs
	del bpy.types.Object.juas_active_limb	

if __name__ == "__main__":
	register()
