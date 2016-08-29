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
from .utils import *

class POSE_OT_juas_roll_bone_move(bpy.types.Operator):
	"""Move Limb up or down in the list"""
	bl_idname = "pose.juas_roll_bone_move"
	bl_label = "Move Bone"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and len(context.object.juas_limbs[context.object.juas_active_limb].roll_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb  = armature.juas_active_limb
		index_bone  = armature.juas_limbs[index_limb].active_roll_bone

		if self.direction == "UP":
			new_index = index_bone - 1
		elif self.direction == "DOWN":
			new_index = index_bone + 1
		else:
			new_index = index_bone

		if new_index < len(armature.juas_limbs[index_limb].roll_bones) and new_index >= 0:
			armature.juas_limbs[index_limb].roll_bones.move(index_bone, new_index)
			armature.juas_limbs[index_limb].active_roll_bone = new_index

		return {'FINISHED'}

class POSE_OT_juas_roll_bone_add(bpy.types.Operator):
	"""Add a new Bone"""
	bl_idname = "pose.juas_roll_bone_add"
	bl_label = "Add Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juas_active_limb

		bone = armature.juas_limbs[index_limb].roll_bones.add()
		if context.active_pose_bone:
			bone.name = context.active_pose_bone.name
		armature.juas_limbs[index_limb].active_roll_bone = len(armature.juas_limbs[index_limb].roll_bones) - 1

		return {'FINISHED'}

class POSE_OT_juas_roll_bone_remove(bpy.types.Operator):

	"""Remove the current Bone"""
	bl_idname = "pose.juas_roll_bone_remove"
	bl_label = "Remove Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and len(context.object.juas_limbs[context.object.juas_active_limb].roll_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juas_active_limb
		index_bone = armature.juas_limbs[index_limb].active_roll_bone

		armature.juas_limbs[index_limb].roll_bones.remove(armature.juas_limbs[index_limb].active_roll_bone)
		len_ = len(armature.juas_limbs[index_limb].roll_bones)
		if (armature.juas_limbs[index_limb].active_roll_bone > (len_ - 1) and len_ > 0):
			armature.juas_limbs[index_limb].active_roll_bone = len(armature.juas_limbs[index_limb].roll_bones) - 1

		return {'FINISHED'}

class POSE_OT_juas_select_bone_move(bpy.types.Operator):
	"""Move Bone up or down in the list"""
	bl_idname = "pose.juas_select_bone_move"
	bl_label = "Move Bone"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and len(context.object.juas_limbs[context.object.juas_active_limb].select_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb  = armature.juas_active_limb
		index_bone  = armature.juas_limbs[index_limb].active_select_bone

		if self.direction == "UP":
			new_index = index_bone - 1
		elif self.direction == "DOWN":
			new_index = index_bone + 1
		else:
			new_index = index_bone

		if new_index < len(armature.juas_limbs[index_limb].select_bones) and new_index >= 0:
			armature.juas_limbs[index_limb].select_bones.move(index_bone, new_index)
			armature.juas_limbs[index_limb].active_select_bone = new_index

		return {'FINISHED'}

class POSE_OT_juas_select_bone_add(bpy.types.Operator):
	"""Add a new Bone"""
	bl_idname = "pose.juas_select_bone_add"
	bl_label = "Add Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juas_active_limb

		bone = armature.juas_limbs[index_limb].select_bones.add()
		if context.active_pose_bone:
			bone.name = context.active_pose_bone.name
		armature.juas_limbs[index_limb].active_select_bone = len(armature.juas_limbs[index_limb].select_bones) - 1

		return {'FINISHED'}

class POSE_OT_juas_select_bone_remove(bpy.types.Operator):

	"""Remove the current Bone"""
	bl_idname = "pose.juas_select_bone_remove"
	bl_label = "Remove Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and len(context.object.juas_limbs[context.object.juas_active_limb].select_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juas_active_limb
		index_bone = armature.juas_limbs[index_limb].active_select_bone

		armature.juas_limbs[index_limb].select_bones.remove(armature.juas_limbs[index_limb].active_select_bone)
		len_ = len(armature.juas_limbs[index_limb].select_bones)
		if (armature.juas_limbs[index_limb].active_select_bone > (len_ - 1) and len_ > 0):
			armature.juas_limbs[index_limb].active_select_bone = len(armature.juas_limbs[index_limb].select_bones) - 1

		return {'FINISHED'}

class POSE_OT_juas_add_bone_move(bpy.types.Operator):
	"""Move Bone up or down in the list"""
	bl_idname = "pose.juas_add_bone_move"
	bl_label = "Move Bone"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and len(context.object.juas_limbs[context.object.juas_active_limb].add_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb  = armature.juas_active_limb
		index_bone  = armature.juas_limbs[index_limb].active_add_bone

		if self.direction == "UP":
			new_index = index_bone - 1
		elif self.direction == "DOWN":
			new_index = index_bone + 1
		else:
			new_index = index_bone

		if new_index < len(armature.juas_limbs[index_limb].add_bones) and new_index >= 0:
			armature.juas_limbs[index_limb].add_bones.move(index_bone, new_index)
			armature.juas_limbs[index_limb].active_add_bone = new_index

		return {'FINISHED'}

class POSE_OT_juas_add_bone_add(bpy.types.Operator):
	"""Add a new Bone"""
	bl_idname = "pose.juas_add_bone_add"
	bl_label = "Add Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juas_active_limb

		bone = armature.juas_limbs[index_limb].add_bones.add()
		armature.juas_limbs[index_limb].active_add_bone = len(armature.juas_limbs[index_limb].add_bones) - 1

		return {'FINISHED'}

class POSE_OT_juas_add_bone_remove(bpy.types.Operator):

	"""Remove the current Bone"""
	bl_idname = "pose.juas_add_bone_remove"
	bl_label = "Remove Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and len(context.object.juas_limbs[context.object.juas_active_limb].add_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juas_active_limb
		index_bone = armature.juas_limbs[index_limb].active_add_bone

		armature.juas_limbs[index_limb].add_bones.remove(armature.juas_limbs[index_limb].active_add_bone)
		len_ = len(armature.juas_limbs[index_limb].add_bones)
		if (armature.juas_limbs[index_limb].active_add_bone > (len_ - 1) and len_ > 0):
			armature.juas_limbs[index_limb].active_add_bone = len(armature.juas_limbs[index_limb].add_bones) - 1

		return {'FINISHED'}


class POSE_OT_juas_limb_move(bpy.types.Operator):
	"""Move Limb up or down in the list"""
	bl_idname = "pose.juas_limb_move"
	bl_label = "Move Limb"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):
		armature = context.object
		index   = armature.juas_active_limb

		if self.direction == "UP":
			new_index = index - 1
		elif self.direction == "DOWN":
			new_index = index + 1
		else:
			new_index = index

		if new_index < len(armature.juas_limbs) and new_index >= 0:
			armature.juas_limbs.move(index, new_index)
			armature.juas_active_limb = new_index

		return {'FINISHED'}

class POSE_OT_juas_limb_add(bpy.types.Operator):
	"""Add a new Limb"""
	bl_idname = "pose.juas_limb_add"
	bl_label = "Add Limb"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"

	def execute(self, context):
		armature = context.object

		if len(armature.juas_limbs) == 0 and len(addonpref().sides) == 0:
			init_sides(context)

		limb = armature.juas_limbs.add()
		limb.name = "Limb.%d" % len(armature.juas_limbs)

		#Set default values
		limb.interaction.autoswitch = addonpref().autoswitch
		limb.interaction.autoswitch_keyframe = addonpref().autoswitch_keyframe
		limb.interaction.autodisplay = addonpref().autodisplay
		limb.interaction.autodisplay_data.type = addonpref().autodisplay_type
		limb.interaction.autokeyframe = addonpref().autokeyframe
		limb.interaction.autokeyframe_data.type = addonpref().autokeyframe_type
		limb.layout.basic = addonpref().basic

		armature.juas_active_limb = len(armature.juas_limbs) - 1

		return {'FINISHED'}

class POSE_OT_juas_limb_remove(bpy.types.Operator):
	"""Remove the current Limb"""
	bl_idname = "pose.juas_limb_remove"
	bl_label = "Remove Limb"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE"

	def execute(self, context):
		armature = context.object

		armature.juas_limbs.remove(armature.juas_active_limb)
		len_ = len(armature.juas_limbs)
		if (armature.juas_active_limb > (len_ - 1) and len_ > 0):
			armature.juas_active_limb = len(armature.juas_limbs) - 1

		return {'FINISHED'}

class POSE_OT_juas_side_move(bpy.types.Operator):
	"""Move Side up or down in the list"""
	bl_idname = "pose.juas_side_move"
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

class POSE_OT_juas_side_add(bpy.types.Operator):
	"""Add a new Side"""
	bl_idname = "pose.juas_side_add"
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

class POSE_OT_juas_side_remove(bpy.types.Operator):
	"""Remove the current Side"""
	bl_idname = "pose.juas_side_remove"
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


class POSE_OT_juas_side_init(bpy.types.Operator):
	"""Init Side"""
	bl_idname = "pose.juas_side_init"
	bl_label = "Init Side"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return True

	def execute(self, context):
		init_sides(context)

		return {'FINISHED'}

class POSE_OT_juas_limb_select_bone_from_selection(bpy.types.Operator):
	"""Set selected bones to colection"""
	bl_idname = "pose.juas_limb_selected_bones_select"
	bl_label = "Add selected bones"
	bl_options = {'REGISTER'}

	bone = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):
		armature = context.object
		selected = context.selected_pose_bones

		if self.bone == "roll_bones":
			for bone in selected:
				if bone.name not in [roll.name for roll in armature.juas_limbs[armature.juas_active_limb].roll_bones]:
					new_bone = armature.juas_limbs[armature.juas_active_limb].roll_bones.add()
					new_bone.name = bone.name
					armature.juas_limbs[armature.juas_active_limb].active_roll_bone = len(armature.juas_limbs[armature.juas_active_limb].roll_bones) - 1
		elif self.bone == "select_bones":
			for bone in selected:
				if bone.name not in [sel.name for sel in armature.juas_limbs[armature.juas_active_limb].select_bones]:
					new_bone = armature.juas_limbs[armature.juas_active_limb].select_bones.add()
					new_bone.name = bone.name
					armature.juas_limbs[armature.juas_active_limb].active_select_bone = len(armature.juas_limbs[armature.juas_active_limb].select_bones) - 1
		elif self.bone == "stay_bones":
			for bone in selected:
				if bone.name not in [stay.name for stay in armature.juas_limbs[armature.juas_active_limb].stay_bones]:
					new_bone = armature.juas_limbs[armature.juas_active_limb].stay_bones.add()
					new_bone.name = bone.name
					armature.juas_limbs[armature.juas_active_limb].active_stay_bone = len(armature.juas_limbs[armature.juas_active_limb].stay_bones) - 1
		return {'FINISHED'}

class POSE_OT_juas_stay_bone_move(bpy.types.Operator):
	"""Move Limb up or down in the list"""
	bl_idname = "pose.juas_stay_bone_move"
	bl_label = "Move Bone"
	bl_options = {'REGISTER'}

	direction = bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and len(context.object.juas_limbs[context.object.juas_active_limb].stay_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb  = armature.juas_active_limb
		index_bone  = armature.juas_limbs[index_limb].active_stay_bone

		if self.direction == "UP":
			new_index = index_bone - 1
		elif self.direction == "DOWN":
			new_index = index_bone + 1
		else:
			new_index = index_bone

		if new_index < len(armature.juas_limbs[index_limb].stay_bones) and new_index >= 0:
			armature.juas_limbs[index_limb].stay_bones.move(index_bone, new_index)
			armature.juas_limbs[index_limb].active_stay_bone = new_index

		return {'FINISHED'}

class POSE_OT_juas_stay_bone_add(bpy.types.Operator):
	"""Add a new Bone"""
	bl_idname = "pose.juas_stay_bone_add"
	bl_label = "Add Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juas_active_limb

		bone = armature.juas_limbs[index_limb].stay_bones.add()
		if context.active_pose_bone:
			bone.name = context.active_pose_bone.name
		armature.juas_limbs[index_limb].active_stay_bone = len(armature.juas_limbs[index_limb].stay_bones) - 1

		return {'FINISHED'}

class POSE_OT_juas_stay_bone_remove(bpy.types.Operator):

	"""Remove the current Bone"""
	bl_idname = "pose.juas_stay_bone_remove"
	bl_label = "Remove Bone"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and len(context.object.juas_limbs[context.object.juas_active_limb].stay_bones) > 0

	def execute(self, context):
		armature = context.object
		index_limb = armature.juas_active_limb
		index_bone = armature.juas_limbs[index_limb].active_stay_bone

		armature.juas_limbs[index_limb].stay_bones.remove(armature.juas_limbs[index_limb].active_stay_bone)
		len_ = len(armature.juas_limbs[index_limb].stay_bones)
		if (armature.juas_limbs[index_limb].active_stay_bone > (len_ - 1) and len_ > 0):
			armature.juas_limbs[index_limb].active_stay_bone = len(armature.juas_limbs[index_limb].stay_bones) - 1

		return {'FINISHED'}

class POSE_OT_juas_limb_select_bone(bpy.types.Operator):
	"""Set active bone to limb bone"""
	bl_idname = "pose.juas_limb_select_bone"
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
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):
		armature = context.object
		if context.active_pose_bone:
			bone_name = context.active_pose_bone.name

		if self.level == 0:
			if self.bone == "roll_bone":
				armature.juas_limbs[armature.juas_active_limb].roll_bones[armature.juas_limbs[armature.juas_active_limb].active_roll_bone].name = bone_name
			elif self.bone == "stay_bone":
				armature.juas_limbs[armature.juas_active_limb].stay_bones[armature.juas_limbs[armature.juas_active_limb].active_stay_bone].name = bone_name
			elif self.bone == "add_bone":
				if self.bone_side == "FK":
					armature.juas_limbs[armature.juas_active_limb].add_bones[armature.juas_limbs[armature.juas_active_limb].active_add_bone].name_FK = bone_name
				else:
					armature.juas_limbs[armature.juas_active_limb].add_bones[armature.juas_limbs[armature.juas_active_limb].active_add_bone].name_IK = bone_name
			elif self.bone == "select_bone":
				armature.juas_limbs[armature.juas_active_limb].select_bones[armature.juas_limbs[armature.juas_active_limb].active_select_bone].name = bone_name
			else:
				armature.juas_limbs[armature.juas_active_limb][self.bone] = bone_name

		elif self.level == 2:
			armature.juas_limbs[armature.juas_active_limb][self.level_1][self.level_2] = bone_name
			if self.bone == "switch_bone":
				armature.juas_limbs[armature.juas_active_limb].interaction.autoswitch_data.bone = bone_name
		elif self.level == 3:
			armature.juas_limbs[armature.juas_active_limb][self.level_1][self.level_2][self.level_3] = bone_name
			if self.level_1 == "interaction" and self.level_2 == "autoswitch_data" and self.level_3 == "bone":
				armature.juas_limbs[armature.juas_active_limb].layout.switch_bone = bone_name


		return {'FINISHED'}

class POSE_OT_juas_limb_select_layer(bpy.types.Operator):
	"""Set active layers to layer data"""
	bl_idname = "pose.juas_limb_select_layer"
	bl_label = "Select Limb layer"
	bl_options = {'REGISTER'}

	layer   =   bpy.props.StringProperty()

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):
		armature = context.object
		if context.active_pose_bone:
			bone_name = context.active_pose_bone.name

		if self.layer == "layer_ik":
			armature.juas_limbs[armature.juas_active_limb].interaction.autodisplay_data.layer_ik = armature.data.bones[bone_name].layers
		elif self.layer == "layer_fk":
			armature.juas_limbs[armature.juas_active_limb].interaction.autodisplay_data.layer_fk = armature.data.bones[bone_name].layers

		return {'FINISHED'}

def register():
	bpy.utils.register_class(POSE_OT_juas_limb_move)
	bpy.utils.register_class(POSE_OT_juas_limb_add)
	bpy.utils.register_class(POSE_OT_juas_limb_remove)

	bpy.utils.register_class(POSE_OT_juas_side_move)
	bpy.utils.register_class(POSE_OT_juas_side_add)
	bpy.utils.register_class(POSE_OT_juas_side_remove)
	bpy.utils.register_class(POSE_OT_juas_side_init)

	bpy.utils.register_class(POSE_OT_juas_roll_bone_move)
	bpy.utils.register_class(POSE_OT_juas_roll_bone_add)
	bpy.utils.register_class(POSE_OT_juas_roll_bone_remove)

	bpy.utils.register_class(POSE_OT_juas_stay_bone_move)
	bpy.utils.register_class(POSE_OT_juas_stay_bone_add)
	bpy.utils.register_class(POSE_OT_juas_stay_bone_remove)

	bpy.utils.register_class(POSE_OT_juas_select_bone_move)
	bpy.utils.register_class(POSE_OT_juas_select_bone_add)
	bpy.utils.register_class(POSE_OT_juas_select_bone_remove)

	bpy.utils.register_class(POSE_OT_juas_add_bone_move)
	bpy.utils.register_class(POSE_OT_juas_add_bone_add)
	bpy.utils.register_class(POSE_OT_juas_add_bone_remove)

	bpy.utils.register_class(POSE_OT_juas_limb_select_bone)
	bpy.utils.register_class(POSE_OT_juas_limb_select_bone_from_selection)
	bpy.utils.register_class(POSE_OT_juas_limb_select_layer)

def unregister():
	bpy.utils.unregister_class(POSE_OT_juas_limb_move)
	bpy.utils.unregister_class(POSE_OT_juas_limb_add)
	bpy.utils.unregister_class(POSE_OT_juas_limb_remove)

	bpy.utils.unregister_class(POSE_OT_juas_side_move)
	bpy.utils.unregister_class(POSE_OT_juas_side_add)
	bpy.utils.unregister_class(POSE_OT_juas_side_remove)
	bpy.utils.unregister_class(POSE_OT_juas_side_init)

	bpy.utils.unregister_class(POSE_OT_juas_roll_bone_move)
	bpy.utils.unregister_class(POSE_OT_juas_roll_bone_add)
	bpy.utils.unregister_class(POSE_OT_juas_roll_bone_remove)

	bpy.utils.unregister_class(POSE_OT_juas_stay_bone_move)
	bpy.utils.unregister_class(POSE_OT_juas_stay_bone_add)
	bpy.utils.unregister_class(POSE_OT_juas_stay_bone_remove)

	bpy.utils.unregister_class(POSE_OT_juas_select_bone_move)
	bpy.utils.unregister_class(POSE_OT_juas_select_bone_add)
	bpy.utils.unregister_class(POSE_OT_juas_select_bone_remove)

	bpy.utils.unregister_class(POSE_OT_juas_add_bone_move)
	bpy.utils.unregister_class(POSE_OT_juas_add_bone_add)
	bpy.utils.unregister_class(POSE_OT_juas_add_bone_remove)

	bpy.utils.unregister_class(POSE_OT_juas_limb_select_bone)
	bpy.utils.unregister_class(POSE_OT_juas_limb_select_bone_from_selection)
	bpy.utils.unregister_class(POSE_OT_juas_limb_select_layer)
