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
from .utils import *

class POSE_OT_reinit_bone_move(bpy.types.Operator):
	"""Move Limb up or down in the list"""
	bl_idname = "pose.reinit_bone_move"
	bl_label = "Move Bone"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and len(context.object.limbs[context.object.active_limb].reinit_bones) > 0
		
	def execute(self, context):
		armature = context.object
		index_limb  = armature.active_limb
		index_bone  = armature.limbs[index_limb].active_reinit_bone
		
		if self.direction == "UP":
			new_index = index_bone - 1
		elif self.direction == "DOWN":
			new_index = index_bone + 1
		else:
			new_index = index_bone
			
		if new_index < len(armature.limbs[index_limb].reinit_bones) and new_index >= 0:
			armature.limbs[index_limb].reinit_bones.move(index_bone, new_index)
			armature.limbs[index_limb].active_reinit_bone = new_index
		
		return {'FINISHED'}
		
class POSE_OT_reinit_bone_add(bpy.types.Operator):
	"""Add a new Bone"""
	bl_idname = "pose.reinit_bone_add"
	bl_label = "Add Bone"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
				
	def execute(self, context):
		armature = context.object
		index_limb = armature.active_limb

		bone = armature.limbs[index_limb].reinit_bones.add()
		if context.active_pose_bone:
			bone.name = context.active_pose_bone.name
		armature.limbs[index_limb].active_reinit_bone = len(armature.limbs[index_limb].reinit_bones) - 1
		
		return {'FINISHED'}
		
class POSE_OT_reinit_bone_remove(bpy.types.Operator):

	"""Remove the current Bone"""
	bl_idname = "pose.reinit_bone_remove"
	bl_label = "Remove Bone"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and len(context.object.limbs[context.object.active_limb].reinit_bones) > 0
				
	def execute(self, context):
		armature = context.object   
		index_limb = armature.active_limb
		index_bone = armature.limbs[index_limb].active_reinit_bone
		
		armature.limbs[index_limb].reinit_bones.remove(armature.limbs[index_limb].active_reinit_bone)
		len_ = len(armature.limbs[index_limb].reinit_bones)
		if (armature.limbs[index_limb].active_reinit_bone > (len_ - 1) and len_ > 0):
			armature.limbs[index_limb].active_reinit_bone = len(armature.limbs[index_limb].reinit_bones) - 1
			
		return {'FINISHED'}  
		
class POSE_OT_select_bone_move(bpy.types.Operator):
	"""Move Bone up or down in the list"""
	bl_idname = "pose.select_bone_move"
	bl_label = "Move Bone"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and len(context.object.limbs[context.object.active_limb].select_bones) > 0
		
	def execute(self, context):
		armature = context.object
		index_limb  = armature.active_limb
		index_bone  = armature.limbs[index_limb].active_select_bone
		
		if self.direction == "UP":
			new_index = index_bone - 1
		elif self.direction == "DOWN":
			new_index = index_bone + 1
		else:
			new_index = index_bone
			
		if new_index < len(armature.limbs[index_limb].select_bones) and new_index >= 0:
			armature.limbs[index_limb].select_bones.move(index_bone, new_index)
			armature.limbs[index_limb].active_select_bone = new_index
		
		return {'FINISHED'}
		
class POSE_OT_select_bone_add(bpy.types.Operator):
	"""Add a new Bone"""
	bl_idname = "pose.select_bone_add"
	bl_label = "Add Bone"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
				
	def execute(self, context):
		armature = context.object
		index_limb = armature.active_limb

		bone = armature.limbs[index_limb].select_bones.add()
		if context.active_pose_bone:
			bone.name = context.active_pose_bone.name
		armature.limbs[index_limb].active_select_bone = len(armature.limbs[index_limb].select_bones) - 1
		
		return {'FINISHED'}
		
class POSE_OT_select_bone_remove(bpy.types.Operator):

	"""Remove the current Bone"""
	bl_idname = "pose.select_bone_remove"
	bl_label = "Remove Bone"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and len(context.object.limbs[context.object.active_limb].select_bones) > 0
				
	def execute(self, context):
		armature = context.object   
		index_limb = armature.active_limb
		index_bone = armature.limbs[index_limb].active_select_bone
		
		armature.limbs[index_limb].select_bones.remove(armature.limbs[index_limb].active_select_bone)
		len_ = len(armature.limbs[index_limb].select_bones)
		if (armature.limbs[index_limb].active_select_bone > (len_ - 1) and len_ > 0):
			armature.limbs[index_limb].active_select_bone = len(armature.limbs[index_limb].select_bones) - 1
			
		return {'FINISHED'}
		
class POSE_OT_add_bone_move(bpy.types.Operator):
	"""Move Bone up or down in the list"""
	bl_idname = "pose.add_bone_move"
	bl_label = "Move Bone"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and len(context.object.limbs[context.object.active_limb].add_bones) > 0
		
	def execute(self, context):
		armature = context.object
		index_limb  = armature.active_limb
		index_bone  = armature.limbs[index_limb].active_add_bone
		
		if self.direction == "UP":
			new_index = index_bone - 1
		elif self.direction == "DOWN":
			new_index = index_bone + 1
		else:
			new_index = index_bone
			
		if new_index < len(armature.limbs[index_limb].add_bones) and new_index >= 0:
			armature.limbs[index_limb].add_bones.move(index_bone, new_index)
			armature.limbs[index_limb].active_add_bone = new_index
		
		return {'FINISHED'}
		
class POSE_OT_add_bone_add(bpy.types.Operator):
	"""Add a new Bone"""
	bl_idname = "pose.add_bone_add"
	bl_label = "Add Bone"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
				
	def execute(self, context):
		armature = context.object
		index_limb = armature.active_limb

		bone = armature.limbs[index_limb].add_bones.add()
		armature.limbs[index_limb].active_add_bone = len(armature.limbs[index_limb].add_bones) - 1
		
		return {'FINISHED'}
		
class POSE_OT_add_bone_remove(bpy.types.Operator):

	"""Remove the current Bone"""
	bl_idname = "pose.add_bone_remove"
	bl_label = "Remove Bone"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and len(context.object.limbs[context.object.active_limb].add_bones) > 0
				
	def execute(self, context):
		armature = context.object   
		index_limb = armature.active_limb
		index_bone = armature.limbs[index_limb].active_add_bone
		
		armature.limbs[index_limb].add_bones.remove(armature.limbs[index_limb].active_add_bone)
		len_ = len(armature.limbs[index_limb].add_bones)
		if (armature.limbs[index_limb].active_add_bone > (len_ - 1) and len_ > 0):
			armature.limbs[index_limb].active_add_bone = len(armature.limbs[index_limb].add_bones) - 1
			
		return {'FINISHED'}  
		
		
class POSE_OT_limb_move(bpy.types.Operator):
	"""Move Limb up or down in the list"""
	bl_idname = "pose.limb_move"
	bl_label = "Move Limb"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
		
	def execute(self, context):
		armature = context.object
		index   = armature.active_limb
		
		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index
			
		if new_index < len(armature.limbs) and new_index >= 0:
			armature.limbs.move(index, new_index)
			armature.active_limb = new_index
		
		return {'FINISHED'}
			
class POSE_OT_limb_add(bpy.types.Operator):
	"""Add a new Limb"""
	bl_idname = "pose.limb_add"
	bl_label = "Add Limb"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"
				
	def execute(self, context):
		armature = context.object
		
		if len(armature.limbs) == 0 and len(addonpref().sides) == 0:
			init_sides(context)

		limb = armature.limbs.add()
		limb.name = "Limb.%d" % len(armature.limbs)
		
		#Set default values
		limb.interaction.autoswitch = addonpref().autoswitch
		limb.interaction.autoswitch_keyframe = addonpref().autoswitch_keyframe
		limb.interaction.autodisplay = addonpref().autodisplay
		limb.interaction.autodisplay_data.type = addonpref().autodisplay_type
		limb.interaction.autokeyframe = addonpref().autokeyframe
		limb.interaction.autokeyframe_data.type = addonpref().autokeyframe_type
		limb.layout.basic = addonpref().basic
		
		armature.active_limb = len(armature.limbs) - 1
		
		return {'FINISHED'}
		
class POSE_OT_limb_remove(bpy.types.Operator):
	"""Remove the current Limb"""
	bl_idname = "pose.limb_remove"
	bl_label = "Remove Limb"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"
				
	def execute(self, context):
		armature = context.object   
		
		armature.limbs.remove(armature.active_limb)
		len_ = len(armature.limbs)
		if (armature.active_limb > (len_ - 1) and len_ > 0):
			armature.active_limb = len(armature.limbs) - 1
			
		return {'FINISHED'}   
		
class POSE_OT_side_move(bpy.types.Operator):
	"""Move Side up or down in the list"""
	bl_idname = "pose.side_move"
	bl_label = "Move Side"
	bl_options = {'REGISTER'}
	
	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(addonpref().sides) > 0
		
	def execute(self, context):
		index   = addonpref().active_side
		
		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index
			
		if new_index < len(addonpref().sides) and new_index >= 0:
			addonpref().sides.move(index, new_index)
			addonpref().active_side = new_index
		
		return {'FINISHED'}
		
class POSE_OT_side_add(bpy.types.Operator):
	"""Add a new Side"""
	bl_idname = "pose.side_add"
	bl_label = "Add Side"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"
				
	def execute(self, context):
		side = addonpref().sides.add()
		side.name = "Side.%d" % len(addonpref().sides)
		addonpref().active_side = len(addonpref().sides) - 1
		
		return {'FINISHED'}
		
class POSE_OT_side_remove(bpy.types.Operator):
	"""Remove the current Side"""
	bl_idname = "pose.side_remove"
	bl_label = "Remove Side"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"
				
	def execute(self, context):	
		addonpref().sides.remove(addonpref().active_side)
		len_ = len(addonpref().sides)
		if (addonpref().active_side > (len_ - 1) and len_ > 0):
			addonpref().active_side = len(addonpref().sides) - 1
			
		return {'FINISHED'}   
		

class POSE_OT_side_init(bpy.types.Operator):
	"""Init Side"""
	bl_idname = "pose.side_init"
	bl_label = "Init Side"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return True
				
	def execute(self, context):	
		init_sides(context)
			
		return {'FINISHED'}  	
		
class POSE_OT_limb_select_bone_from_selection(bpy.types.Operator):
	"""Set selected bones to colection"""
	bl_idname = "pose.limb_selected_bones_select"
	bl_label = "Add selected bones"
	bl_options = {'REGISTER'}	
	
	bone = bpy.props.StringProperty()
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
		
	def execute(self, context):
		armature = context.object
		selected = context.selected_pose_bones
		
		if self.bone == "reinit_bones":
			for bone in selected:
				if bone.name not in [reinit.name for reinit in armature.limbs[armature.active_limb].reinit_bones]:
					new_bone = armature.limbs[armature.active_limb].reinit_bones.add()
					new_bone.name = bone.name
					armature.limbs[armature.active_limb].active_reinit_bone = len(armature.limbs[armature.active_limb].reinit_bones) - 1
		elif self.bone == "select_bones":
			for bone in selected:
				if bone.name not in [sel.name for sel in armature.limbs[armature.active_limb].select_bones]:
					new_bone = armature.limbs[armature.active_limb].select_bones.add()
					new_bone.name = bone.name
					armature.limbs[armature.active_limb].active_select_bone = len(armature.limbs[armature.active_limb].select_bones) - 1
		return {'FINISHED'}  
		
class POSE_OT_limb_select_bone(bpy.types.Operator):
	"""Set active bone to limb bone"""
	bl_idname = "pose.limb_select_bone"
	bl_label = "Select Limb bone"
	bl_options = {'REGISTER'}
	
	bone = bpy.props.StringProperty()
	bone_side =  bpy.props.StringProperty()
	level = bpy.props.IntProperty()
	level_1 = bpy.props.StringProperty()
	level_2 = bpy.props.StringProperty()
	level_3 = bpy.props.StringProperty()
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
				
	def execute(self, context):
		armature = context.object
		if context.active_pose_bone:
			bone_name = context.active_pose_bone.name
			
		if self.level == 0:
			if self.bone == "reinit_bone":
				armature.limbs[armature.active_limb].reinit_bones[armature.limbs[armature.active_limb].active_reinit_bone].name = bone_name
			elif self.bone == "add_bone":
				if self.bone_side == "FK":
					armature.limbs[armature.active_limb].add_bones[armature.limbs[armature.active_limb].active_add_bone].name_FK = bone_name
				else:
					armature.limbs[armature.active_limb].add_bones[armature.limbs[armature.active_limb].active_add_bone].name_IK = bone_name
			elif self.bone == "select_bone":
				armature.limbs[armature.active_limb].select_bones[armature.limbs[armature.active_limb].active_select_bone].name = bone_name
			else:
				armature.limbs[armature.active_limb][self.bone] = bone_name

		elif self.level == 2:
			armature.limbs[armature.active_limb][self.level_1][self.level_2] = bone_name
			if self.bone == "switch_bone":
				armature.limbs[armature.active_limb].interaction.autoswitch_data.bone = bone_name
		elif self.level == 3:
			armature.limbs[armature.active_limb][self.level_1][self.level_2][self.level_3] = bone_name
			if self.level_1 == "interaction" and self.level_2 == "autoswitch_data" and self.level_3 == "bone":
				armature.limbs[armature.active_limb].layout.switch_bone = bone_name
		
	
		return {'FINISHED'}   
		
class POSE_OT_limb_select_layer(bpy.types.Operator):
	"""Set active layers to layer data"""
	bl_idname = "pose.limb_select_layer"
	bl_label = "Select Limb layer"
	bl_options = {'REGISTER'}
	
	layer   =   bpy.props.StringProperty()
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
				
	def execute(self, context):
		armature = context.object
		if context.active_pose_bone:
			bone_name = context.active_pose_bone.name
			
		if self.layer == "layer_ik":
			armature.limbs[armature.active_limb].interaction.autodisplay_data.layer_ik = armature.data.bones[bone_name].layers
		elif self.layer == "layer_fk":
			armature.limbs[armature.active_limb].interaction.autodisplay_data.layer_fk = armature.data.bones[bone_name].layers
	
		return {'FINISHED'}   

def register():
	bpy.utils.register_class(POSE_OT_limb_move)
	bpy.utils.register_class(POSE_OT_limb_add)
	bpy.utils.register_class(POSE_OT_limb_remove)
	
	bpy.utils.register_class(POSE_OT_side_move)
	bpy.utils.register_class(POSE_OT_side_add)
	bpy.utils.register_class(POSE_OT_side_remove)
	bpy.utils.register_class(POSE_OT_side_init)
	
	bpy.utils.register_class(POSE_OT_reinit_bone_move)
	bpy.utils.register_class(POSE_OT_reinit_bone_add)
	bpy.utils.register_class(POSE_OT_reinit_bone_remove)
	
	bpy.utils.register_class(POSE_OT_select_bone_move)
	bpy.utils.register_class(POSE_OT_select_bone_add)
	bpy.utils.register_class(POSE_OT_select_bone_remove)
	
	bpy.utils.register_class(POSE_OT_add_bone_move)
	bpy.utils.register_class(POSE_OT_add_bone_add)
	bpy.utils.register_class(POSE_OT_add_bone_remove)
	
	bpy.utils.register_class(POSE_OT_limb_select_bone)
	bpy.utils.register_class(POSE_OT_limb_select_bone_from_selection)
	bpy.utils.register_class(POSE_OT_limb_select_layer)

def unregister():
	bpy.utils.unregister_class(POSE_OT_limb_move)
	bpy.utils.unregister_class(POSE_OT_limb_add)
	bpy.utils.unregister_class(POSE_OT_limb_remove)
	
	bpy.utils.unregister_class(POSE_OT_side_move)
	bpy.utils.unregister_class(POSE_OT_side_add)
	bpy.utils.unregister_class(POSE_OT_side_remove)
	bpy.utils.unregister_class(POSE_OT_side_init)
	
	bpy.utils.unregister_class(POSE_OT_reinit_bone_move)
	bpy.utils.unregister_class(POSE_OT_reinit_bone_add)
	bpy.utils.unregister_class(POSE_OT_reinit_bone_remove)
	
	bpy.utils.unregister_class(POSE_OT_select_bone_move)
	bpy.utils.unregister_class(POSE_OT_select_bone_add)
	bpy.utils.unregister_class(POSE_OT_select_bone_remove)
	
	bpy.utils.unregister_class(POSE_OT_add_bone_move)
	bpy.utils.unregister_class(POSE_OT_add_bone_add)
	bpy.utils.unregister_class(POSE_OT_add_bone_remove)
	
	bpy.utils.unregister_class(POSE_OT_limb_select_bone)
	bpy.utils.unregister_class(POSE_OT_limb_select_bone_from_selection)
	bpy.utils.unregister_class(POSE_OT_limb_select_layer)

