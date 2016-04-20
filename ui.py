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

class POSE_UL_SideList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name_L", text="", emboss=False)
			layout.prop(item, "name_R", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'		
		
class POSE_UL_LimbList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_UL_ReInitBoneList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_UL_SelectBoneList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_UL_AddBoneList(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.prop(item, "name_FK", text="", emboss=False)
			layout.prop(item, "name_IK", text="", emboss=False)
			
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			
class POSE_MT_limb_specials(bpy.types.Menu):
	bl_label = "Limb Specials"

	def draw(self, context):
		layout = self.layout
	
		op = layout.operator("pose.limb_copy", icon='COPY_ID', text="Copy Limb")
		op.mirror = False
		op = layout.operator("pose.limb_copy", icon='ARROW_LEFTRIGHT', text="Mirror Copy Limb")
		op.mirror = True
	
class POSE_PT_Limb_livesnap(bpy.types.Panel):
	bl_label = "Live Snapping"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoSnap"
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and context.mode == 'POSE'
		
	def populate_ops_param(self, context, op):
		armature = context.object
	
		op.root = armature.limbs[armature.active_limb].root
		
		op.global_scale = armature.limbs[armature.active_limb].global_scale
		op.ik_type = armature.limbs[armature.active_limb].ik_type
		op.ik_scale_type = armature.limbs[armature.active_limb].ik_scale_type
		op.fk_scale_type = armature.limbs[armature.active_limb].fk_scale_type
		op.ik_location_type = armature.limbs[armature.active_limb].ik_location_type
		op.fk_location_type = armature.limbs[armature.active_limb].fk_location_type
		op.with_limb_end_fk	= armature.limbs[armature.active_limb].with_limb_end_fk
		op.with_limb_end_ik	= armature.limbs[armature.active_limb].with_limb_end_ik
		op.with_reinit_bones   = armature.limbs[armature.active_limb].with_reinit_bones
		op.with_add_bones      = armature.limbs[armature.active_limb].with_add_bones
		
		op.ik1 = armature.limbs[armature.active_limb].ik1
		op.ik2 = armature.limbs[armature.active_limb].ik2
		op.ik3 = armature.limbs[armature.active_limb].ik3
		op.ik4 = armature.limbs[armature.active_limb].ik4
		op.ik5 = armature.limbs[armature.active_limb].ik5
		
		op.fk1 = armature.limbs[armature.active_limb].fk1
		op.fk2 = armature.limbs[armature.active_limb].fk2
		op.fk3 = armature.limbs[armature.active_limb].fk3
		op.fk4 = armature.limbs[armature.active_limb].fk4
		
		op.ik_scale = armature.limbs[armature.active_limb].ik_scale
		op.fk_scale = armature.limbs[armature.active_limb].fk_scale
		op.ik_location = armature.limbs[armature.active_limb].ik_location
		op.fk_location = armature.limbs[armature.active_limb].fk_location
		
		for item_src in armature.limbs[armature.active_limb].reinit_bones:
			item_dst = op.reinit_bones.add()
			item_dst.name = item_src.name
		if len(armature.limbs[armature.active_limb].reinit_bones) == 0:
			op.with_reinit_bones = False
			
		for item_src in armature.limbs[armature.active_limb].add_bones:
			item_dst = op.add_bones.add()
			item_dst.name_FK = item_src.name_FK
			item_dst.name_IK = item_src.name_IK
		if len(armature.limbs[armature.active_limb].add_bones) == 0:
			op.with_add_bones = False
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		if armature.limbs[armature.active_limb].layout.basic == True:
			row = layout.row()
			box = row.box()
			if armature.limbs[armature.active_limb].layout.on_select == True:
				if context.active_pose_bone.name not in [bone.name for bone in armature.limbs[armature.active_limb].select_bones]:
					row_ = box.row()
					row_.label("Preview Only : Bone is not in selected list", icon='ERROR')
			if armature.limbs[armature.active_limb].layout.display_name == True:
				row_ = box.row()
				row_.label(armature.limbs[armature.active_limb].name)
			row_ = box.row()
			op = row_.operator("pose.limb_switch_ikfk", text=armature.limbs[armature.active_limb].layout.fk2ik_label)
			op.layout_basic = armature.limbs[armature.active_limb].layout.basic
			op.switch_way = "FK2IK"
			op.autoswitch =  armature.limbs[armature.active_limb].interaction.autoswitch
			if armature.limbs[armature.active_limb].interaction.autoswitch == True:
				op.autoswitch_data_bone = armature.limbs[armature.active_limb].interaction.autoswitch_data.bone
				op.autoswitch_data_property = armature.limbs[armature.active_limb].interaction.autoswitch_data.property
			self.populate_ops_param(context, op)
			
			row_ = box.row()
			op = row_.operator("pose.limb_switch_ikfk", text=armature.limbs[armature.active_limb].layout.ik2fk_label)
			op.layout_basic = armature.limbs[armature.active_limb].layout.basic
			op.switch_way = "IK2FK"
			self.populate_ops_param(context, op)
			
		else:
			label = ""
			try:
				if int(armature.pose.bones[armature.limbs[armature.active_limb].layout.switch_bone].get(armature.limbs[armature.active_limb].layout.switch_property)) == 1.0 and armature.limbs[armature.active_limb].layout.switch_invert == "IKIS0":
					label = armature.limbs[armature.active_limb].layout.ik2fk_label
				elif int(armature.pose.bones[armature.limbs[armature.active_limb].layout.switch_bone].get(armature.limbs[armature.active_limb].layout.switch_property)) == 1.0 and armature.limbs[armature.active_limb].layout.switch_invert == "FKIS0":
					label = armature.limbs[armature.active_limb].layout.fk2ik_label
				if int(armature.pose.bones[armature.limbs[armature.active_limb].layout.switch_bone].get(armature.limbs[armature.active_limb].layout.switch_property)) == 0.0 and armature.limbs[armature.active_limb].layout.switch_invert == "IKIS0":
					label = armature.limbs[armature.active_limb].layout.fk2ik_label
				elif int(armature.pose.bones[armature.limbs[armature.active_limb].layout.switch_bone].get(armature.limbs[armature.active_limb].layout.switch_property)) == 0.0 and armature.limbs[armature.active_limb].layout.switch_invert == "FKIS0":
					label = armature.limbs[armature.active_limb].layout.ik2fk_label
			except:
				label = ""
			row = layout.row()
			box = row.box()
			if armature.limbs[armature.active_limb].layout.on_select == True:
				if context.active_pose_bone.name not in [bone.name for bone in armature.limbs[armature.active_limb].select_bones]:
					row_ = box.row()
					row_.label("Preview Only : Bone is not in selected list", icon='ERROR')
			if armature.limbs[armature.active_limb].layout.display_name == True:
				row_ = box.row()
				row_.label(armature.limbs[armature.active_limb].name)
			row_ = box.row()
			op = row_.operator("pose.limb_switch_ikfk", text=label)
			op.layout_basic = armature.limbs[armature.active_limb].layout.basic
			op.switch_bone = armature.limbs[armature.active_limb].layout.switch_bone
			op.switch_property = armature.limbs[armature.active_limb].layout.switch_property
			op.switch_invert   = armature.limbs[armature.active_limb].layout.switch_invert
			op.autoswitch =  armature.limbs[armature.active_limb].interaction.autoswitch
			op.autoswitch_keyframe = armature.limbs[armature.active_limb].interaction.autoswitch_keyframe
			if armature.limbs[armature.active_limb].interaction.autoswitch == True:
				op.autoswitch_data_bone = armature.limbs[armature.active_limb].interaction.autoswitch_data.bone
				op.autoswitch_data_property = armature.limbs[armature.active_limb].interaction.autoswitch_data.property
			op.autodisplay =  armature.limbs[armature.active_limb].interaction.autodisplay
			if armature.limbs[armature.active_limb].interaction.autodisplay == True:
				op.autodisplay_data_type = armature.limbs[armature.active_limb].interaction.autodisplay_data.type
				if armature.limbs[armature.active_limb].interaction.autodisplay_data.type == "LAYER":
					op.autodisplay_data_layer_ik = armature.limbs[armature.active_limb].interaction.autodisplay_data.layer_ik
					op.autodisplay_data_layer_fk = armature.limbs[armature.active_limb].interaction.autodisplay_data.layer_fk
				elif armature.limbs[armature.active_limb].interaction.autodisplay_data.type == "HIDE":
					op.autodisplay_data_bone = armature.limbs[armature.active_limb].interaction.autodisplay_data.bone
					op.autodisplay_data_property = armature.limbs[armature.active_limb].interaction.autodisplay_data.property
					op.autodisplay_data_invert = armature.limbs[armature.active_limb].interaction.autodisplay_data.invert
			op.autokeyframe =  armature.limbs[armature.active_limb].interaction.autokeyframe
			if armature.limbs[armature.active_limb].interaction.autokeyframe == True:
				op.autokeyframe_data_type          = armature.limbs[armature.active_limb].interaction.autokeyframe_data.type
				op.autokeyframe_data_keying_set_FK = armature.limbs[armature.active_limb].interaction.autokeyframe_data.keying_set_FK
				op.autokeyframe_data_keying_set_IK = armature.limbs[armature.active_limb].interaction.autokeyframe_data.keying_set_IK
			self.populate_ops_param(context, op)
			row_ = box.row()
			if label == "":
				row_.label("Wrong layout data", icon="ERROR")
			if armature.limbs[armature.active_limb].interaction.autoswitch == True:
				try:
					int(armature.pose.bones[armature.limbs[armature.active_limb].interaction.autoswitch_data.bone].get(armature.limbs[armature.active_limb].interaction.autoswitch_data.property))
					row_ = box.row()
					row_.prop(armature.limbs[armature.active_limb].interaction, "autoswitch", text="AutoSwitch")
					if armature.limbs[armature.active_limb].interaction.autoswitch_keyframe == True:
						row_.prop(armature.limbs[armature.active_limb].interaction, "autoswitch_keyframe", text="Keyframe")
					row_.enabled = False
					
					#check if multiple limb use same bone for storing data
					bones = []
					for limb in armature.limbs:
						if limb.interaction.autoswitch == True:
							if limb.interaction.autoswitch_data.bone_store in bones:
								row_ = box.row()
								row_.label("Multiple 'AutoSwitch' use same Bone to store data", icon="ERROR")
								break
							bones.append(limb.interaction.autoswitch_data.bone_store)
				except:
					row_ = box.row()
					row_.label("Wrong Autoswitch Data", icon="ERROR")
					
			if armature.limbs[armature.active_limb].interaction.autodisplay == True:
				if armature.limbs[armature.active_limb].interaction.autodisplay_data.bone_store not in context.active_object.data.bones.keys():
					row_ = box.row()
					row_.label("Wrong AutoDisplay data", icon="ERROR")
				else:
					if armature.limbs[armature.active_limb].interaction.autodisplay_data.type == "HIDE":
						try:
							int(armature.pose.bones[armature.limbs[armature.active_limb].interaction.autodisplay_data.bone].get(armature.limbs[armature.active_limb].interaction.autodisplay_data.property))
							row_ = box.row()
							row_.prop(armature.limbs[armature.active_limb].interaction, "autodisplay", text="AutoDisplay")
							row_.enabled = False
							#check if multiple limb use same bone for storing data
							bones = []
							for limb in armature.limbs:
								if limb.interaction.autodisplay == True:
									if limb.interaction.autodisplay_data.bone_store in bones:
										row_ = box.row()
										row_.label("Multiple 'AutoDisplay' use same Bone to store data", icon="ERROR")
										break
									bones.append(limb.interaction.autodisplay_data.bone_store)
						except:
							row_ = box.row()
							row_.label("Wrong AutoDisplay Data", icon="ERROR")
					else: #Layer
						row_ = box.row()
						row_.prop(armature.limbs[armature.active_limb].interaction, "autodisplay", text="AutoDisplay")
						row_.enabled = False
						#check if multiple limb use same bone for storing data
						bones = []
						for limb in armature.limbs:
							if limb.interaction.autodisplay == True:
								if limb.interaction.autodisplay_data.bone_store in bones:
									row_ = box.row()
									row_.label("Multiple 'AutoDisplay' use same Bone to store data", icon="ERROR")
									break
								bones.append(limb.interaction.autodisplay_data.bone_store)						
							
			if armature.limbs[armature.active_limb].interaction.autokeyframe == True:
				if armature.limbs[armature.active_limb].interaction.autokeyframe_data.bone_store not in context.active_object.data.bones.keys():
					row_ = box.row()
					row_.label("Wrong AutoKeyframe data", icon="ERROR")
					#TODO : add check keying sets ?
				else:
					row_ = box.row()
					row_.prop(armature.limbs[armature.active_limb].interaction, "autokeyframe", text="AutoKeyframe")
					row_.enabled = False
					#check if multiple limb use same bone for storing data
					bones = []
					for limb in armature.limbs:
						if limb.interaction.autokeyframe == True:
							if limb.interaction.autokeyframe_data.bone_store in bones:
								row_ = box.row()
								row_.label("Multiple 'AutoKeyframe' use same Bone to store data", icon="ERROR")
								break
							bones.append(limb.interaction.autokeyframe_data.bone_store)
							
							
class POSE_PT_Snap_Generate(bpy.types.Panel):
	bl_label = "Generate"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoSnap"
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and context.mode == 'POSE' and addonpref().generated_enable == True
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
		row = layout.row()
		row.prop(armature.generation, "view_location")
		row = layout.row()
		row.prop(armature.generation, "panel_name")
		if armature.generation.view_location == "TOOLS":
			row = layout.row()
			row.prop(armature.generation, "tab_tool")
		row = layout.row()
		row.operator("pose.generate_snapping", text="Generate")
		
class POSE_PT_Limbs(bpy.types.Panel):
	bl_label = "Limbs"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoSnap"
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and context.mode == 'POSE'
				
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		row = layout.row()
		row.template_list("POSE_UL_LimbList", "", armature, "limbs", armature, "active_limb")
		
		col = row.column()
		row = col.column(align=True)
		row.operator("pose.limb_add", icon="ZOOMIN", text="")
		row.operator("pose.limb_remove", icon="ZOOMOUT", text="")
		row.menu("POSE_MT_limb_specials", icon='DOWNARROW_HLT', text="")
			
		if len(context.active_object.limbs) > 0:
			row = col.column(align=True)
			row.separator()
			row.operator("pose.limb_move", icon='TRIA_UP', text="").direction = 'UP'
			row.operator("pose.limb_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
		
class POSE_PT_LimbDetailBones(bpy.types.Panel):
	bl_label = "Limb Detail -  Bones"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoSnap"	
	
	@classmethod
	def poll(self, context):
		armature = context.active_object
		return armature and armature.type == "ARMATURE" and len(armature.limbs) > 0 and context.mode == 'POSE' and armature.limbs[armature.active_limb].display.bone == True
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
		limb = armature.limbs[armature.active_limb]
		
		row_ = layout.row()
		box = row_.box()
		row__ = box.row()
		row__.prop(limb, "global_scale")
		if limb.global_scale == True:
			row__ = box.row()
			col = row__.column()
			row = col.column(align=True)
			row.prop_search(limb, "root", armature.data, "bones", text="Root")
			col = row__.column()
			row = col.column(align=True)
			op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.bone = "root"
			op.level = 0

		row_ = layout.row()
		box_ = row_.box()
		row___ = box_.row()

		box = row___.box()
		row__ = box.row()
		row__.label("Main IK chain")
		row__= box.row()
		col = row__.column()
		row = col.column(align=True)
		row.prop_search(limb, "ik1", armature.data, "bones", text="IK1")
		col = row__.column()
		row = col.column(align=True)
		op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
		op.bone = "ik1"
		op.level = 0
		
		row__ = box.row()
		col = row__.column()
		row = col.column(align=True)
		row.prop_search(limb, "ik2", armature.data, "bones", text="IK2")
		col = row__.column()
		row = col.column(align=True)
		op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
		op.bone = "ik2"
		op.level = 0
		
		row__ = box.row()
		col = row__.column()
		row = col.column(align=True)
		row.prop_search(limb, "ik3", armature.data, "bones", text="IK Target")
		col = row__.column()
		row = col.column(align=True)
		op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
		op.bone = "ik3"
		op.level = 0

		row___ = box_.row()
		box = row___.box()
		row__ = box.row()
		row__.prop(limb, "ik_type")
		if limb.ik_type == "POLE":
			row__ = box.row()
			row_ = row__.row()
			col = row_.column()
			row = col.column(align=True)
			row.prop_search(limb, "ik4", armature.data, "bones", text="IK Pole")
			col = row_.column()
			row = col.column(align=True)
			op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.bone = "ik4"	
			op.level = 0
		
		row___ = box_.row()
		box = row___.box()
		row__ = box.row()
		row__.prop(limb, "with_limb_end_ik", text="Use IK limb end")
		if limb.with_limb_end_ik == True:
			row__ = box.row()
			row_ = row__.row()
			col = row_.column()
			row = col.column(align=True)
			row.prop_search(limb, "ik5", armature.data, "bones", text="IK toe")
			col = row_.column()
			row = col.column(align=True)
			op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="") 
			op.bone = "ik5" 
			op.level = 0

		row___ = box_.row()
		box = row___.box()
		row__ = box.row()
		row__.prop(limb, "ik_scale_type")
		if limb.ik_scale_type == "PARENT":
			row__ = box.row()
			row_ = row__.row()
			col = row_.column()
			row = col.column(align=True)
			row.prop_search(limb, "ik_scale", armature.data, "bones", text="IK Scale")
			col = row_.column()
			row = col.column(align=True)
			op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.bone = "ik_scale"
			op.level = 0

		row___ = box_.row()
		box = row___.box()
		row__ = box.row()
		row__.prop(limb, "ik_location_type")
		if limb.ik_location_type == "PARENT":
			row__ = box.row()
			row_ = row__.row()
			col = row_.column()
			row = col.column(align=True)
			row.prop_search(limb, "ik_location", armature.data, "bones", text="IK Location")
			col = row_.column()
			row = col.column(align=True)
			op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.bone = "ik_location"
			op.level = 0
			

		row___ = box_.row()
		box = row___.box()
		row__ = box.row()
		row__.prop(limb, "with_reinit_bones", text="Roll/Rock bones to reinit")
		if limb.with_reinit_bones == True:
			row__ = box.row()
			op = row__.operator("pose.limb_selected_bones_select", text="Fill from selection")
			op.bone = "reinit_bones"
			row__= box.row()
			row__.template_list("POSE_UL_ReInitBoneList", "", armature.limbs[armature.active_limb], "reinit_bones", armature.limbs[armature.active_limb], "active_reinit_bone")
			
			col = row__.column()
			row = col.column(align=True)
			row.operator("pose.reinit_bone_add", icon="ZOOMIN", text="")
			row.operator("pose.reinit_bone_remove", icon="ZOOMOUT", text="")
				
			row = col.column(align=True)
			row.separator()
			row.operator("pose.reinit_bone_move", icon='TRIA_UP', text="").direction = 'UP'
			row.operator("pose.reinit_bone_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
			
			if len(armature.limbs[armature.active_limb].reinit_bones) > 0:
				row_ = box.row()
				col = row_.column()
				row = col.column(align=True)
				row.prop_search(armature.limbs[armature.active_limb].reinit_bones[armature.limbs[armature.active_limb].active_reinit_bone], "name", armature.data, "bones", text="Bone")
				col = row_.column()
				row = col.column(align=True)
				op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
				op.bone = "reinit_bone"
				op.level = 0

			
		row_ = layout.row()
		box_ = row_.box()
		row___ = box_.row()

		box = row___.box()
		row__ = box.row()
		row__.label("Main FK chain")
		row__= box.row()
		col = row__.column()
		row = col.column(align=True)
		row.prop_search(limb, "fk1", armature.data, "bones", text="FK1")
		col = row__.column()
		row = col.column(align=True)
		op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
		op.bone = "fk1"
		op.level = 0
		
		row__= box.row()
		col = row__.column()
		row = col.column(align=True)
		row.prop_search(limb, "fk2", armature.data, "bones", text="FK2")
		col = row__.column()
		row = col.column(align=True)
		op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
		op.bone = "fk2"
		op.level = 0
		
		row__= box.row()
		col = row__.column()
		row = col.column(align=True)
		row.prop_search(limb, "fk3", armature.data, "bones", text="FK3")
		col = row__.column()
		row = col.column(align=True)
		op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
		op.bone = "fk3"
		op.level = 0

		
		row___ = box_.row()
		box = row___.box()
		row__ = box.row()
		row__.prop(limb, "with_limb_end_fk", text="Use FK limb end")
		if limb.with_limb_end_fk == True:
			row__ = box.row()
			row_ = row__.row()
			col = row_.column()
			row = col.column(align=True)
			row.prop_search(limb, "fk4", armature.data, "bones", text="FK toe")
			col = row_.column()
			row = col.column(align=True)
			op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="") 
			op.bone = "fk4"  
			op.level = 0
			
		row___ = box_.row()
		box = row___.box()
		row__ = box.row()
		row__.prop(limb, "fk_scale_type")
		if limb.fk_scale_type == "PARENT":
			row__ = box.row()
			row_ = row__.row()
			col = row_.column()
			row = col.column(align=True)
			row.prop_search(limb, "fk_scale", armature.data, "bones", text="FK Scale")
			col = row_.column()
			row = col.column(align=True)
			op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.bone = "fk_scale"
			op.level = 0

		row___ = box_.row()
		box = row___.box()
		row__ = box.row()
		row__.prop(limb, "fk_location_type")
		if limb.fk_location_type == "PARENT":
			row__ = box.row()
			row_ = row__.row()
			col = row_.column()
			row = col.column(align=True)
			row.prop_search(limb, "fk_location", armature.data, "bones", text="FK Location")
			col = row_.column()
			row = col.column(align=True)
			op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")	
			op.bone = "fk_location"
			op.level = 0
			
		row_ = layout.row()
		row_.prop(limb, "with_add_bones", text="Additional Bones")
		row_ = layout.row()
		if limb.with_add_bones == True:

			box  = row_.box()
			row__= box.row()
			row__.template_list("POSE_UL_AddBoneList", "", armature.limbs[armature.active_limb], "add_bones", armature.limbs[armature.active_limb], "active_add_bone")
			
			col = row__.column()
			row = col.column(align=True)
			row.operator("pose.add_bone_add", icon="ZOOMIN", text="")
			row.operator("pose.add_bone_remove", icon="ZOOMOUT", text="")
				
			row = col.column(align=True)
			row.separator()
			row.operator("pose.add_bone_move", icon='TRIA_UP', text="").direction = 'UP'
			row.operator("pose.add_bone_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
			
			if len(armature.limbs[armature.active_limb].add_bones) > 0:
				row_ = box.row()
				col = row_.column()
				row = col.column(align=True)
				row.prop_search(armature.limbs[armature.active_limb].add_bones[armature.limbs[armature.active_limb].active_add_bone], "name_FK", armature.data, "bones", text="Bone FK")
				col = row_.column()
				row = col.column(align=True)
				op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
				op.bone = "add_bone"
				op.level = 0
				op.bone_side = 'FK'
				row_ = box.row()
				col = row_.column()
				row = col.column(align=True)
				row.prop_search(armature.limbs[armature.active_limb].add_bones[armature.limbs[armature.active_limb].active_add_bone], "name_IK", armature.data, "bones", text="Bone IK")
				col = row_.column()
				row = col.column(align=True)
				op = row.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
				op.bone = "add_bone"
				op.level = 0
				op.bone_side = 'IK'
		
class POSE_PT_LimbDetail(bpy.types.Panel):
	bl_label = "Limb Detail"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoSnap"
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and context.mode == 'POSE'
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
		limb = armature.limbs[armature.active_limb]
	
		row = layout.row()
		row.prop(limb, "name", text="name")

		row = layout.row()
		row.prop(limb.display, "bone")
		row = layout.row()
		row.prop(limb.display, "layout")
		row = layout.row()
		row.prop(limb.display, "interaction")
		if limb.layout.basic == True:
			row.enabled = False
			
class POSE_PT_LimbDetailLayout(bpy.types.Panel):
	bl_label = "Limb Detail - Layout"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoSnap"

	@classmethod
	def poll(self, context):
		armature = context.active_object
		return armature and armature.type == "ARMATURE" and len(armature.limbs) > 0 and context.mode == 'POSE' and armature.limbs[armature.active_limb].display.layout == True
		
	def draw(self, context):
		layout = self.layout
		armature = context.active_object
		limb = armature.limbs[armature.active_limb]
		
		row = layout.row()
		box = row.box()
		row_ = box.row()
		row_.prop(limb.layout, "basic", "Basic Layout")
		
		row_ = box.row()
		row_.prop(limb.layout, "fk2ik_label", "Label fk2ik")
		row_ = box.row()
		row_.prop(limb.layout, "ik2fk_label", "Label ik2fk")
		
		if limb.layout.basic == False:
			row = layout.row()
			box = row.box()
			row_ = box.row()
			col = row_.column()
			row__ = col.column(align=True)
			row__.prop_search(limb.layout, "switch_bone", armature.data, "bones", text="Switch Bone")
			col = row_.column()
			row__ = col.row()
			op = row__.operator("pose.limb_select_bone", icon="BONE_DATA", text="")	
			op.bone = "switch_bone"
			op.level = 2
			op.level_1 = "layout"
			op.level_2 = "switch_bone"
			row_ = box.row()
			row_.prop(limb.layout, "switch_property", text="Switch Property")
			row_.prop(limb.layout, "switch_invert", text="way")
			
		row = layout.row()
		box = row.row()
		row_ = box.row()
		row_.prop(limb.layout, "display_name", text="Display Name")
		
		row = layout.row()
		box = row.row()
		row_ = box.row()
		row_.prop(limb.layout, "on_select", text="Display On Select")
		if limb.layout.on_select == True:
			row = layout.row()
			op = row.operator("pose.limb_selected_bones_select", text="Fill from selection")
			op.bone = "select_bones"
			row = layout.row()
			row.template_list("POSE_UL_SelectBoneList", "", armature.limbs[armature.active_limb], "select_bones", armature.limbs[armature.active_limb], "active_select_bone")
			
			col = row.column()
			row_ = col.column(align=True)
			row_.operator("pose.select_bone_add", icon="ZOOMIN", text="")
			row_.operator("pose.select_bone_remove", icon="ZOOMOUT", text="")
				
			row_ = col.column(align=True)
			row_.separator()
			row_.operator("pose.select_bone_move", icon='TRIA_UP', text="").direction = 'UP'
			row_.operator("pose.select_bone_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
			
			if len(armature.limbs[armature.active_limb].select_bones) > 0:
				row = layout.row()
				col = row.column()
				row_ = col.column(align=True)
				row_.prop_search(armature.limbs[armature.active_limb].select_bones[armature.limbs[armature.active_limb].active_select_bone], "name", armature.data, "bones", text="Bone")
				col = row.column()
				row_ = col.column(align=True)
				op = row_.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
				op.bone = "select_bone"
				op.level = 0
			
class POSE_PT_LimbDetailInteraction(bpy.types.Panel):
	bl_label = "Limb Detail - Interaction"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoSnap"

	@classmethod
	def poll(self, context):
		armature = context.active_object
		return armature and armature.type == "ARMATURE" and len(armature.limbs) > 0 and context.mode == 'POSE' and armature.limbs[armature.active_limb].display.interaction == True
		
	def draw(self, context):
		layout = self.layout
		armature = context.active_object
		limb = armature.limbs[armature.active_limb]
		
		row = layout.row()
		row.prop(limb.interaction, "autoswitch", text="Auto Switch")
		if limb.interaction.autoswitch == True:
			row = layout.row()
			box = row.box()
			row_ = box.row()
			col = row_.column()
			row__ = col.row()
			row__.prop_search(limb.interaction.autoswitch_data, "bone", armature.data, "bones", text="Bone")
			col = row_.column()
			row__ = col.row()
			op = row__.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.level = 3
			op.level_1 = "interaction"
			op.level_2 = "autoswitch_data"
			op.level_3 = "bone"
			row_ = box.row()
			col = row_.column()
			row__ = col.row()
			row__.prop_search(limb.interaction.autoswitch_data, "bone_store", armature.data, "bones", text="Bone (to store data)")
			col = row_.column()
			row__ = col.row()
			op = row__.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.level = 3
			op.level_1 = "interaction"
			op.level_2 = "autoswitch_data"
			op.level_3 = "bone_store"
			row_ = box.row()
			row_.prop(limb.interaction.autoswitch_data, "property", text="Property")
			row_ = box.row()
			row_.prop(limb.interaction, "autoswitch_keyframe", text="Keyframe")
			
		row = layout.row()
		row.prop(limb.interaction, "autodisplay", text="Auto Display")
		if limb.interaction.autodisplay == True:
			row = layout.row()
			box = row.box()
			row_ = box.row()
			col = row_.column()
			row__ = col.row()
			row__.prop_search(limb.interaction.autodisplay_data, "bone_store", armature.data, "bones", text="Bone (to store data)")
			col = row_.column()
			row__ = col.row()
			op = row__.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.level = 3
			op.level_1 = "interaction"
			op.level_2 = "autodisplay_data"
			op.level_3 = "bone_store"
			row_ = box.row()
			row_.prop(limb.interaction.autodisplay_data, "type", text="Type")
			row_ = box.row()
			if limb.interaction.autodisplay_data.type == "LAYER":
				col = row_.column()
				row__ = col.row()
				row__.prop(limb.interaction.autodisplay_data, "layer_ik", text="Layer IK")
				col = row_.column()
				row__ = col.row()
				op = row__.operator("pose.limb_select_layer", icon="BONE_DATA", text="")
				op.layer = "layer_ik"
				row_ = box.row()
				col = row_.column()
				row__ = col.row()
				row__.prop(limb.interaction.autodisplay_data, "layer_fk", text="Layer FK")
				col = row_.column()
				row__ = col.row()
				op = row__.operator("pose.limb_select_layer", icon="BONE_DATA", text="")
				op.layer = "layer_fk"
			elif limb.interaction.autodisplay_data.type == "HIDE":
				col = row_.column()
				row__ = col.row()
				row__.prop_search(limb.interaction.autodisplay_data, "bone", armature.data, "bones", text="Bone")
				col = row_.column()
				row__ = col.row()
				op = row__.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
				op.level = 3
				op.level_1 = "interaction"
				op.level_2 = "autodisplay_data"
				op.level_3 = "bone"
				row_ = box.row()
				row_.prop(limb.interaction.autodisplay_data, "property", text="Property")
				row_.prop(limb.interaction.autodisplay_data, "invert", text="Invert")
				
		row = layout.row()
		row.prop(limb.interaction, "autokeyframe", text="Auto Keyframe Chain")
		if limb.interaction.autokeyframe == True:
			row = layout.row()
			box = row.box()
			row_ = box.row()
			row_.prop(limb.interaction.autokeyframe_data, "type", text="Type")
			row_ = box.row()
			col = row_.column()
			row__ = col.row()
			row__.prop_search(limb.interaction.autokeyframe_data, "bone_store", armature.data, "bones", text="Bone (to store data)")
			col = row_.column()
			row__ = col.row()
			op = row__.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.level = 3
			op.level_1 = "interaction"
			op.level_2 = "autokeyframe_data"
			op.level_3 = "bone_store"
			if limb.interaction.autokeyframe_data.type == "KEYING_SET":
				row_ = box.row()
				row_.prop_search(limb.interaction.autokeyframe_data, "keying_set_FK", context.scene, "keying_sets", text="Keying Set FK")
				row_ = box.row()
				row_.prop_search(limb.interaction.autokeyframe_data, "keying_set_IK", context.scene, "keying_sets", text="Keying Set IK")
			
def register():
	bpy.utils.register_class(POSE_UL_SideList)
	bpy.utils.register_class(POSE_UL_LimbList)
	bpy.utils.register_class(POSE_UL_ReInitBoneList)
	bpy.utils.register_class(POSE_UL_AddBoneList)
	bpy.utils.register_class(POSE_UL_SelectBoneList)
	
	bpy.utils.register_class(POSE_MT_limb_specials)
	
	bpy.utils.register_class(POSE_PT_Limbs)
	bpy.utils.register_class(POSE_PT_LimbDetail)
	bpy.utils.register_class(POSE_PT_LimbDetailBones)
	bpy.utils.register_class(POSE_PT_LimbDetailLayout)
	bpy.utils.register_class(POSE_PT_LimbDetailInteraction)
	bpy.utils.register_class(POSE_PT_Limb_livesnap)
	bpy.utils.register_class(POSE_PT_Snap_Generate)

def unregister():
	bpy.utils.unregister_class(POSE_UL_SideList)
	bpy.utils.unregister_class(POSE_UL_LimbList)
	bpy.utils.unregister_class(POSE_UL_ReInitBoneList)
	bpy.utils.unregister_class(POSE_UL_AddBoneList)
	bpy.utils.unregister_class(POSE_UL_SelectBoneList)
	
	bpy.utils.unregister_class(POSE_MT_limb_specials)
	
	bpy.utils.unregister_class(POSE_PT_Limbs) 
	bpy.utils.unregister_class(POSE_PT_LimbDetail)
	bpy.utils.unregister_class(POSE_PT_LimbDetailBones)
	bpy.utils.unregister_class(POSE_PT_LimbDetailLayout)
	bpy.utils.unregister_class(POSE_PT_LimbDetailInteraction)
	bpy.utils.unregister_class(POSE_PT_Limb_livesnap)
	bpy.utils.unregister_class(POSE_PT_Snap_Generate)
