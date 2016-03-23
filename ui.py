import bpy

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
			
class POSE_MT_limb_specials(bpy.types.Menu):
	bl_label = "Limb Specials"

	def draw(self, context):
		layout = self.layout
	
		layout.operator("pose.limb_mirror_copy", icon='ARROW_LEFTRIGHT')
	
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
		
	def draw(self, context):
		layout = self.layout
		armature = context.object
		
		if armature.generation.layout_type == "DEFAULT":
			row = layout.row()
			box = row.box()
			row_ = box.row()
			row_.label(armature.limbs[armature.active_limb].name)
			row_ = box.row()
			op = row_.operator("pose.limb_switch_ikfk", text=armature.limbs[armature.active_limb].fk2ik_label)
			op.switch_type = "FORCED"
			op.layout_type = "DEFAULT"
			op.switch_forced_value = "FK2IK"
			op.autoswitch =  armature.limbs[armature.active_limb].interaction.autoswitch
			if armature.limbs[armature.active_limb].interaction.autoswitch == True:
				op.autoswitch_data_bone = armature.limbs[armature.active_limb].interaction.autoswitch_data.bone
				op.autoswitch_data_property = armature.limbs[armature.active_limb].interaction.autoswitch_data.property
			self.populate_ops_param(context, op)
			
			row_ = box.row()
			op = row_.operator("pose.limb_switch_ikfk", text=armature.limbs[armature.active_limb].ik2fk_label)
			op.switch_type = "FORCED"
			op.layout_type = "DEFAULT"
			op.switch_forced_value = "IK2FK"
			self.populate_ops_param(context, op)
			
		elif armature.generation.layout_type == "DEFAULT_SWITCH":
			label = ""
			try:
				if int(armature.pose.bones[armature.limbs[armature.active_limb].switch_bone].get(armature.limbs[armature.active_limb].switch_property)) == 1.0 and armature.limbs[armature.active_limb].switch_invert == False:
					label = armature.limbs[armature.active_limb].ik2fk_label
				elif int(armature.pose.bones[armature.limbs[armature.active_limb].switch_bone].get(armature.limbs[armature.active_limb].switch_property)) == 1.0 and armature.limbs[armature.active_limb].switch_invert == True:
					label = armature.limbs[armature.active_limb].fk2ik_label
				if int(armature.pose.bones[armature.limbs[armature.active_limb].switch_bone].get(armature.limbs[armature.active_limb].switch_property)) == 0.0 and armature.limbs[armature.active_limb].switch_invert == False:
					label = armature.limbs[armature.active_limb].fk2ik_label
				elif int(armature.pose.bones[armature.limbs[armature.active_limb].switch_bone].get(armature.limbs[armature.active_limb].switch_property)) == 0.0 and armature.limbs[armature.active_limb].switch_invert == True:
					label = armature.limbs[armature.active_limb].ik2fk_label
			except:
				label = ""
			row = layout.row()
			box = row.box()
			row_ = box.row()
			row_.label(armature.limbs[armature.active_limb].name)
			row_ = box.row()
			op = row_.operator("pose.limb_switch_ikfk", text=label)
			op.switch_type = "DEDUCTED"
			op.layout_type = "DEFAULT_SWITCH"
			op.switch_bone = armature.limbs[armature.active_limb].switch_bone
			op.switch_property = armature.limbs[armature.active_limb].switch_property
			op.switch_invert   = armature.limbs[armature.active_limb].switch_invert
			op.autoswitch =  armature.limbs[armature.active_limb].interaction.autoswitch
			op.autoswitch_keyframe = armature.limbs[armature.active_limb].interaction.autoswitch_keyframe
			if armature.limbs[armature.active_limb].interaction.autoswitch == True:
				op.autoswitch_data_bone = armature.limbs[armature.active_limb].interaction.autoswitch_data.bone
				op.autoswitch_data_property = armature.limbs[armature.active_limb].interaction.autoswitch_data.property
			op.autodisplay =  armature.limbs[armature.active_limb].interaction.autodisplay
			if armature.limbs[armature.active_limb].interaction.autodisplay == True:
				op.autodisplay_data_type = armature.limbs[armature.active_limb].interaction.autodisplay_data.type
				op.autodisplay_data_layer_ik = armature.limbs[armature.active_limb].interaction.autodisplay_data.layer_ik
				op.autodisplay_data_layer_fk = armature.limbs[armature.active_limb].interaction.autodisplay_data.layer_fk
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
				except:
					row_ = box.row()
					row_.label("Wrong Autoswitch Data", icon="ERROR")
			if armature.limbs[armature.active_limb].interaction.autodisplay == True:
				if armature.limbs[armature.active_limb].interaction.autodisplay_data.bone not in context.active_object.data.bones.keys():
					row_ = box.row()
					row_.label("Wrong AutoDisplay data", icon="ERROR")
				else:
					row_ = box.row()
					row_.prop(armature.limbs[armature.active_limb].interaction, "autodisplay", text="AutoDisplay")
					row_.enabled = False
			
class POSE_PT_Snap_Generate(bpy.types.Panel):
	bl_label = "Generate"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "AutoSnap"
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and context.mode == 'POSE'
		
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

class POSE_PT_layout(bpy.types.Panel):
	bl_label = "Layout"
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
		row.prop(armature.generation, "layout_type")
		
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
		if armature.generation.layout_type != "DEFAULT": #No interaction for DEFAULT layout
			row = layout.row()
			row.prop(limb.display, "interaction")
		else:
			row = layout.row()
			row.label("No Interaction for this Layout")
			
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
		if armature.generation.layout_type == "DEFAULT":
			row = layout.row()
			row.prop(limb, "fk2ik_label", "Label fk2ik")
			row = layout.row()
			row.prop(limb, "ik2fk_label", "Label ik2fk")
		elif armature.generation.layout_type == "DEFAULT_SWITCH":
			row = layout.row()
			row.prop(limb, "fk2ik_label", "Label fk2ik")
			row = layout.row()
			row.prop(limb, "ik2fk_label", "Label ik2fk")
			row = layout.row()
			col = row.column()
			row_ = col.column(align=True)
			row_.prop_search(limb, "switch_bone", armature.data, "bones", text="Switch Bone")
			col = row.column()
			row_ = col.row()
			op = row_.operator("pose.limb_select_bone", icon="BONE_DATA", text="")	
			op.bone = "switch_bone"
			op.level = 0
			row = layout.row()
			row.prop(limb, "switch_property", text="Switch Property")
			row.prop(limb, "switch_invert", text="Invert")
			
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
			row__.prop_search(limb.interaction.autodisplay_data, "bone", armature.data, "bones", text="Bone")
			col = row_.column()
			row__ = col.row()
			op = row__.operator("pose.limb_select_bone", icon="BONE_DATA", text="")
			op.level = 3
			op.level_1 = "interaction"
			op.level_2 = "autodisplay_data"
			op.level_3 = "bone"
			row_ = box.row()
			row_.prop(limb.interaction.autodisplay_data, "type", text="Type")
			row_ = box.row()
			if limb.interaction.autodisplay_data.type == "LAYER":
				row_.prop(limb.interaction.autodisplay_data, "layer_ik", text="Layer IK")
				row_ = box.row()
				row_.prop(limb.interaction.autodisplay_data, "layer_fk", text="Layer FK")
			elif limb.interaction.autodisplay_data.type == "HIDE":
				pass #TODO
			
def register():
	bpy.utils.register_class(POSE_UL_SideList)
	bpy.utils.register_class(POSE_UL_LimbList)
	bpy.utils.register_class(POSE_UL_ReInitBoneList)
	
	bpy.utils.register_class(POSE_MT_limb_specials)
	
	bpy.utils.register_class(POSE_PT_layout)
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
	
	bpy.utils.unregister_class(POSE_MT_limb_specials)
	
	bpy.utils.unregister_class(POSE_PT_layout)
	bpy.utils.unregister_class(POSE_PT_Limbs) 
	bpy.utils.unregister_class(POSE_PT_LimbDetail)
	bpy.utils.unregister_class(POSE_PT_LimbDetailBones)
	bpy.utils.unregister_class(POSE_PT_LimbDetailLayout)
	bpy.utils.unregister_class(POSE_PT_LimbDetailInteraction)
	bpy.utils.unregister_class(POSE_PT_Limb_livesnap)
	bpy.utils.unregister_class(POSE_PT_Snap_Generate)
