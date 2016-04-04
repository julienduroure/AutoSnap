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

import bpy

from .globals import *

class AutoSnapPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	sides = bpy.props.CollectionProperty(type=SideItem) 
	active_side = bpy.props.IntProperty()   
	
	basic = bpy.props.BoolProperty(name="Default Basic On", default=False)
	
	autoswitch = bpy.props.BoolProperty(name="Default AutoSwitch On", default=True)
	autoswitch_keyframe = bpy.props.BoolProperty(name="Default AutoSwitch Keyframe On", default=True)
	autodisplay = bpy.props.BoolProperty(name="Default AutoDisplay On", default=True)
	autokeyframe = bpy.props.BoolProperty(name="Default AutoKeyframe On", default=True)
	
	autodisplay_type  = bpy.props.EnumProperty(name="AutoDisplay Default", items=autodisplay_items, default="LAYER")	
	autokeyframe_type = bpy.props.EnumProperty(name="AutoKeyframe Default", items=autokeyframe_items, default="AVAILABLE")

	def draw(self, context):
		layout = self.layout
		
		row_global    = layout.row()
		col = row_global.column()  	
		
		row = col.row()
		row.prop(self, "basic")
		row = col.row()
		row.prop(self, "autoswitch")
		if self.autoswitch == True:
			row.prop(self, "autoswitch_keyframe")
		row = col.row()
		row.prop(self, "autodisplay")
		row.prop(self, "autodisplay_type")
		row = col.row()
		row.prop(self, "autokeyframe")
		row.prop(self, "autokeyframe_type")
		
		col = row_global.column(align=True)
		row = col.row()
		if len(addonpref().sides) > 0:
			row.template_list("POSE_UL_SideList", "", addonpref(), "sides", addonpref(), "active_side")
		
			col_ = row.column()
			row_ = col_.column(align=True)
			row_.operator("pose.side_add", icon="ZOOMIN", text="")
			row_.operator("pose.side_remove", icon="ZOOMOUT", text="")
			
			row_ = col_.column(align=True)
			row_.separator()
			row_.operator("pose.side_move", icon='TRIA_UP', text="").direction = 'UP'
			row_.operator("pose.side_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

		else:
			row.operator("pose.side_init", text="Init sides, for mirror")
  

def register():
	bpy.utils.register_class(SideItem)
	bpy.utils.register_class(AutoSnapPreferences)

def unregister():
	bpy.utils.unregister_class(SideItem)
	bpy.utils.unregister_class(AutoSnapPreferences)
