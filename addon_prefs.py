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

from .globs import *

class JuAS_Preferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	sides = bpy.props.CollectionProperty(type=JuAS_SideItem)
	active_side = bpy.props.IntProperty()

	basic = bpy.props.BoolProperty(name="Default Basic On", default=False)

	autoswitch = bpy.props.BoolProperty(name="Default AutoSwitch On", default=True)
	autoswitch_keyframe = bpy.props.BoolProperty(name="Default AutoSwitch Keyframe On", default=True)
	autodisplay = bpy.props.BoolProperty(name="Default AutoDisplay On", default=True)
	autokeyframe = bpy.props.BoolProperty(name="Default AutoKeyframe On", default=True)

	autodisplay_type  = bpy.props.EnumProperty(name="AutoDisplay Default", items=autodisplay_items, default="LAYER")
	autokeyframe_type = bpy.props.EnumProperty(name="AutoKeyframe Default", items=autokeyframe_items, default="AVAILABLE")

	generated_enable = bpy.props.BoolProperty(name="Generation enabled", default=False)

	panel_name = bpy.props.StringProperty(name="Default Panel name", default="Snapping")
	tab_tool = bpy.props.StringProperty(name="Default Tab name", default="Snapping")

	category = bpy.props.StringProperty(name="Category", default="AutoSnap", update=update_panel)

	def draw(self, context):
		layout = self.layout

		row_global    = layout.row()
		col = row_global.column()

		box = col.box()
		row = box.row()
		row.prop(self, "basic")
		row = box.row()
		row.prop(self, "autoswitch")
		if self.autoswitch == True:
			row.prop(self, "autoswitch_keyframe")
		row = box.row()
		row.prop(self, "autodisplay")
		row.prop(self, "autodisplay_type")
		row = box.row()
		row.prop(self, "autokeyframe")
		row.prop(self, "autokeyframe_type")

		box = col.box()
		row = box.row()
		row.prop(self, "generated_enable")
		if self.generated_enable == True:
			row = box.row()
			row.prop(self, "panel_name", text="Panel Name")
			row = box.row()
			row.prop(self, "tab_tool", text="Tab Name")

		box = col.box()
		row = box.row()
		row.prop(self, "category")

		col = row_global.column(align=True)
		row = col.row()
		if len(addonpref().sides) > 0:
			row.template_list("POSE_UL_JuAS_SideList", "", addonpref(), "sides", addonpref(), "active_side")

			col_ = row.column()
			row_ = col_.column(align=True)
			row_.operator("pose.juas_side_add", icon="ZOOMIN", text="")
			row_.operator("pose.juas_side_remove", icon="ZOOMOUT", text="")

			row_ = col_.column(align=True)
			row_.separator()
			row_.operator("pose.juas_side_move", icon='TRIA_UP', text="").direction = 'UP'
			row_.operator("pose.juas_side_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

		else:
			row.operator("pose.juas_side_init", text="Init sides, for mirror")

def register():
	bpy.utils.register_class(JuAS_SideItem)
	bpy.utils.register_class(JuAS_Preferences)

def unregister():
	bpy.utils.unregister_class(JuAS_SideItem)
	bpy.utils.unregister_class(JuAS_Preferences)
