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
import mathutils
import math
import uuid
import inspect

from .globs import *
from .utils import *
from .ui_texts import *

def get_poll_snapping_op(context):
	return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and context.mode == 'POSE'


class POSE_OT_juas_limb_copy(bpy.types.Operator):
	"""Copy active limb, with mirror option"""
	bl_idname = "pose.juas_limb_copy"
	bl_label = "Copy Limb"
	bl_options = {'REGISTER'}

	mirror = bpy.props.BoolProperty(name="Mirror", default=False)

	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0

	def execute(self, context):

		if self.mirror == True:
			fct = get_symm_name
		else:
			fct = get_name

		if len(addonpref().sides) == 0:
			init_sides(context)

		armature = context.object
		src_limb_index = armature.juas_active_limb
		dst_limb = armature.juas_limbs.add()

		dst_limb.name = fct(armature.juas_limbs[src_limb_index].name)

		dst_limb.display.bone   = armature.juas_limbs[src_limb_index].display.bone
		dst_limb.display.layout = armature.juas_limbs[src_limb_index].display.layout
		dst_limb.display.interaction = armature.juas_limbs[src_limb_index].display.interaction

		dst_limb.interaction.bone_store = fct(armature.juas_limbs[src_limb_index].interaction.bone_store)

		dst_limb.interaction.autoswitch = armature.juas_limbs[src_limb_index].interaction.autoswitch
		dst_limb.interaction.autoswitch_data.bone = fct(armature.juas_limbs[src_limb_index].interaction.autoswitch_data.bone)
		dst_limb.interaction.autoswitch_data.property = armature.juas_limbs[src_limb_index].interaction.autoswitch_data.property
		dst_limb.interaction.autoswitch_keyframe = armature.juas_limbs[src_limb_index].interaction.autoswitch_keyframe

		dst_limb.interaction.autodisplay = armature.juas_limbs[src_limb_index].interaction.autodisplay
		dst_limb.interaction.autodisplay_data.type = armature.juas_limbs[src_limb_index].interaction.autodisplay_data.type
		dst_limb.interaction.autodisplay_data.layer_ik = armature.juas_limbs[src_limb_index].interaction.autodisplay_data.layer_ik
		dst_limb.interaction.autodisplay_data.layer_fk = armature.juas_limbs[src_limb_index].interaction.autodisplay_data.layer_fk
		dst_limb.interaction.autodisplay_data.bone = fct(armature.juas_limbs[src_limb_index].interaction.autodisplay_data.bone)
		dst_limb.interaction.autodisplay_data.property = armature.juas_limbs[src_limb_index].interaction.autodisplay_data.property
		dst_limb.interaction.autodisplay_data.invert = armature.juas_limbs[src_limb_index].interaction.autodisplay_data.invert

		dst_limb.interaction.autokeyframe = armature.juas_limbs[src_limb_index].interaction.autokeyframe
		dst_limb.interaction.autokeyframe_data.type = armature.juas_limbs[src_limb_index].interaction.autokeyframe_data.type
		dst_limb.interaction.autokeyframe_data.keying_set_FK = armature.juas_limbs[src_limb_index].interaction.autokeyframe_data.keying_set_FK
		dst_limb.interaction.autokeyframe_data.keying_set_IK = armature.juas_limbs[src_limb_index].interaction.autokeyframe_data.keying_set_IK

		dst_limb.layout.basic = armature.juas_limbs[src_limb_index].layout.basic
		dst_limb.layout.fk2ik_label = armature.juas_limbs[src_limb_index].layout.fk2ik_label
		dst_limb.layout.ik2fk_label = armature.juas_limbs[src_limb_index].layout.ik2fk_label
		dst_limb.layout.switch_bone = fct(armature.juas_limbs[src_limb_index].layout.switch_bone)
		dst_limb.layout.switch_property = armature.juas_limbs[src_limb_index].layout.switch_property
		dst_limb.layout.switch_invert = armature.juas_limbs[src_limb_index].layout.switch_invert
		dst_limb.layout.display_name = armature.juas_limbs[src_limb_index].layout.display_name
		dst_limb.layout.on_select = armature.juas_limbs[src_limb_index].layout.on_select

		dst_limb.ik_type = armature.juas_limbs[src_limb_index].ik_type
		dst_limb.ik_scale_type = armature.juas_limbs[src_limb_index].ik_scale_type
		dst_limb.fk_scale_type = armature.juas_limbs[src_limb_index].fk_scale_type
		dst_limb.ik_location_type = armature.juas_limbs[src_limb_index].ik_location_type
		dst_limb.fk_location_type = armature.juas_limbs[src_limb_index].fk_location_type
		dst_limb.global_scale = armature.juas_limbs[src_limb_index].global_scale
		dst_limb.with_limb_end_fk = armature.juas_limbs[src_limb_index].with_limb_end_fk
		dst_limb.with_limb_end_ik = armature.juas_limbs[src_limb_index].with_limb_end_ik
		dst_limb.with_roll_bones = armature.juas_limbs[src_limb_index].with_roll_bones
		dst_limb.with_add_bones = armature.juas_limbs[src_limb_index].with_add_bones
		dst_limb.with_stay_bones = armature.juas_limbs[src_limb_index].with_stay_bones

		dst_limb.root = fct(armature.juas_limbs[src_limb_index].root)

		dst_limb.ik1 = fct(armature.juas_limbs[src_limb_index].ik1)
		dst_limb.ik2 = fct(armature.juas_limbs[src_limb_index].ik2)
		dst_limb.ik3 = fct(armature.juas_limbs[src_limb_index].ik3)
		dst_limb.ik4 = fct(armature.juas_limbs[src_limb_index].ik4)
		dst_limb.ik5 = fct(armature.juas_limbs[src_limb_index].ik5)
		dst_limb.ik_scale = fct(armature.juas_limbs[src_limb_index].ik_scale)
		dst_limb.ik_location = fct(armature.juas_limbs[src_limb_index].ik_location)
		dst_limb.ik_mech_foot = fct(armature.juas_limbs[src_limb_index].ik_mech_foot)

		dst_limb.fk1 = fct(armature.juas_limbs[src_limb_index].fk1)
		dst_limb.fk2 = fct(armature.juas_limbs[src_limb_index].fk2)
		dst_limb.fk3 = fct(armature.juas_limbs[src_limb_index].fk3)
		dst_limb.fk4 = fct(armature.juas_limbs[src_limb_index].fk4)
		dst_limb.fk_scale = fct(armature.juas_limbs[src_limb_index].fk_scale)
		dst_limb.fk_location = fct(armature.juas_limbs[src_limb_index].fk_location)


		for src_bone in armature.juas_limbs[src_limb_index].roll_bones:
			dst_bone = dst_limb.roll_bones.add()
			dst_bone.name = fct(src_bone.name)
		dst_limb.active_roll_bone = armature.juas_limbs[src_limb_index].active_roll_bone

		for src_bone in armature.juas_limbs[src_limb_index].add_bones:
			dst_bone = dst_limb.add_bones.add()
			dst_bone.name_FK = fct(src_bone.name_FK)
			dst_bone.name_IK = fct(src_bone.name_IK)
		dst_limb.active_add_bone = armature.juas_limbs[src_limb_index].active_add_bone

		for src_bone in armature.juas_limbs[src_limb_index].select_bones:
			dst_bone = dst_limb.select_bones.add()
			dst_bone.name = fct(src_bone.name)
		dst_limb.active_select_bone = armature.juas_limbs[src_limb_index].active_select_bone

		for src_bone in armature.juas_limbs[src_limb_index].stay_bones:
			dst_bone = dst_limb.stay_bones.add()
			dst_bone.name = fct(src_bone.name)
		dst_limb.active_stay_bone = armature.juas_limbs[src_limb_index].active_stay_bone

		armature.juas_active_limb = len(armature.juas_limbs) - 1

		return {'FINISHED'}

class POSE_OT_juas_limb_switch_ikfk(bpy.types.Operator):
	"""Switch between IK / FK"""
	bl_idname = "pose.juas_limb_switch_ikfk"
	bl_label = "Switch IK/FK"
	bl_options = {'REGISTER'}

	layout_basic = bpy.props.BoolProperty()

	switch_way = bpy.props.EnumProperty(items=switch_way)

	switch_bone = bpy.props.StringProperty()
	switch_property = bpy.props.StringProperty()
	switch_invert   = bpy.props.EnumProperty(items=switch_invert_items)

	autoswitch = bpy.props.BoolProperty()
	autoswitch_data_bone = bpy.props.StringProperty()
	autoswitch_data_property = bpy.props.StringProperty()
	autoswitch_keyframe = bpy.props.BoolProperty()

	autodisplay = bpy.props.BoolProperty()
	autodisplay_data_type = bpy.props.EnumProperty(items=autodisplay_items)
	autodisplay_data_layer_ik = bpy.props.BoolVectorProperty(name="Layer IK", subtype='LAYER', size = 32)
	autodisplay_data_layer_fk = bpy.props.BoolVectorProperty(name="Layer FK", subtype='LAYER', size = 32)
	autodisplay_data_bone = bpy.props.StringProperty()
	autodisplay_data_property = bpy.props.StringProperty()
	autodisplay_data_invert = bpy.props.BoolProperty()

	autokeyframe = bpy.props.BoolProperty()
	autokeyframe_data_type   = bpy.props.EnumProperty(items=autokeyframe_items)
	autokeyframe_data_keying_set_FK = bpy.props.StringProperty()
	autokeyframe_data_keying_set_IK = bpy.props.StringProperty()

	global_scale = bpy.props.BoolProperty()
	ik_scale_type = bpy.props.EnumProperty(items=scale_type_items)
	fk_scale_type = bpy.props.EnumProperty(items=scale_type_items)
	ik_location_type = bpy.props.EnumProperty(items=location_type_items)
	fk_location_type = bpy.props.EnumProperty(items=location_type_items)
	with_limb_end_fk	= bpy.props.BoolProperty()
	with_limb_end_ik	= bpy.props.BoolProperty()
	with_roll_bones   = bpy.props.BoolProperty()
	with_stay_bones   = bpy.props.BoolProperty()
	with_add_bones      = bpy.props.BoolProperty()
	ik_type = bpy.props.EnumProperty(items=IK_type_items)


	root = bpy.props.StringProperty()
	ik1 = bpy.props.StringProperty()
	ik2 = bpy.props.StringProperty()
	ik3 = bpy.props.StringProperty()
	ik4 = bpy.props.StringProperty()
	ik5 = bpy.props.StringProperty()
	ik_scale = bpy.props.StringProperty()
	ik_location = bpy.props.StringProperty()
	ik_mech_foot = bpy.props.StringProperty()
	fk1 = bpy.props.StringProperty()
	fk2 = bpy.props.StringProperty()
	fk3 = bpy.props.StringProperty()
	fk4 = bpy.props.StringProperty()
	fk_scale = bpy.props.StringProperty()
	fk_location = bpy.props.StringProperty()
	roll_bones = bpy.props.CollectionProperty(type=JuAS_BoneItem)
	add_bones    = bpy.props.CollectionProperty(type=JuAS_BonePairItem)
	stay_bones = bpy.props.CollectionProperty(type=JuAS_BoneItem)

	@classmethod
	def poll(self, context):
		return get_poll_snapping_op(context)

	def layout_check_basic(self, context):
		return True, True

	def layout_check_non_basic(self, context):
		if self.switch_bone == "":
			self.report({'ERROR'}, "Switch Bone must be filled")
			return False, {'CANCELLED'}
		if self.switch_property == "":
			self.report({'ERROR'}, "Switch Bone property must be filled")
			return False, {'CANCELLED'}
		try:
			int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property))
		except:
			self.report({'ERROR'}, "Wrong Bone property")
			return False, {'CANCELLED'}


		return True, True

	def check_available_curve(self, bone_list):
		try:
			curves = bpy.context.active_object.animation_data.action.fcurves
		except:
			return False

		for c in curves:
			try:
				tab_ = c.data_path.split("[")
				if tab_[0] == "pose.bones" and tab_[1].split("]")[0][1:len(tab_[1].split("]")[0])-1] in [bone.name for bone in bone_list]:
					return True
			except:
				pass

		return False

	def layout_check(self, context, layout_basic):
		if layout_basic == True:
			return self.layout_check_basic(context)
		elif layout_basic == False:
			return self.layout_check_non_basic(context)

		self.report({'ERROR'}, "Unknow Layout type")
		return False, {'CANCELLED'}

	def common_check(self, context):
		if self.ik1 == "" or self.ik2 == "" or self.ik3 == "":
			self.report({'ERROR'}, "Main IK chain must be totally filled")
			return False, {'CANCELLED'}
		if self.fk1 == "" or self.fk2 == "" or self.fk3 == "":
			self.report({'ERROR'}, "Main FK chain must be totally filled")
			return False, {'CANCELLED'}
		if self.global_scale == True and self.root == "":
			self.report({'ERROR'}, "Root must be filled")
			return False, {'CANCELLED'}
		if self.with_limb_end_ik == True and self.ik5 == "":
			self.report({'ERROR'}, "IK toe must be filled")
			return False, {'CANCELLED'}
		if self.with_limb_end_fk == True and self.fk4 == "":
			self.report({'ERROR'}, "FK toe must be filled")
			return False, {'CANCELLED'}
		if self.ik_scale_type != "NONE" and self.ik_scale == "":
			self.report({'ERROR'}, "IK scale must be filled")
			return False, {'CANCELLED'}
		if self.fk_scale_type != "NONE" and self.fk_scale == "":
			self.report({'ERROR'}, "FK scale must be filled")
			return False, {'CANCELLED'}
		if self.ik_location_type != "NONE" and self.ik_location == "":
			self.report({'ERROR'}, "IK location must be filled")
			return False, {'CANCELLED'}
		if self.fk_location_type != "NONE" and self.fk_location == "":
			self.report({'ERROR'}, "FK location must be filled")
			return False, {'CANCELLED'}

		if self.with_limb_end_ik == False: #No toe stuff
			self.ik5 = ""
		if self.with_limb_end_fk == False: #No toe stuff
			self.fk4 = ""
		if self.global_scale == False: #No global scale
			self.root = ""
		if self.ik_scale_type == "NONE": #No limb scale
			self.ik_scale = ""
		if self.fk_scale_type == "NONE": #No limb scale
			self.fk_scale = ""
		if self.ik_location_type == "NONE": #No limb location
			self.ik_location = ""
		if self.fk_location_type == "NONE": #No limb location
			self.fk_location = ""

		if self.root != "" and self.root not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.root + " doesn't exist")
			return False, {'CANCELLED'}
		if self.ik1 != "" and self.ik1 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik1 + " doesn't exist")
			return False, {'CANCELLED'}
		if self.ik2 != "" and self.ik2 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik2 + " doesn't exist")
			return False, {'CANCELLED'}
		if self.ik3 != "" and self.ik3 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik3 + " doesn't exist")
			return False, {'CANCELLED'}
		if self.ik5 != "" and self.ik5 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik5 + " doesn't exist")
			return False, {'CANCELLED'}
		if self.ik_scale != "" and self.ik_scale not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik_scale + " doesn't exist")
			return False, {'CANCELLED'}
		if self.ik_location != "" and self.ik_location not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik_location + " doesn't exist")
			return False, {'CANCELLED'}
		if self.ik_mech_foot != "" and self.ik_mech_foot not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik_mech_foot + " doesn't exist")
			return False, {'CANCELLED'}
		if self.fk1 != "" and self.fk1 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.fk1 + " doesn't exist")
			return False, {'CANCELLED'}
		if self.fk2 != "" and self.fk2 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.fk2 + " doesn't exist")
			return False, {'CANCELLED'}
		if self.fk3 != "" and self.fk3 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.fk3 + " doesn't exist")
			return False, {'CANCELLED'}
		if self.fk4 != "" and self.fk4 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.fk4 + " doesn't exist")
			return False, {'CANCELLED'}
		if self.fk_scale != "" and self.fk_scale not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.fk_scale + " doesn't exist")
			return False, {'CANCELLED'}
		if self.fk_location != "" and self.fk_location not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.fk_location + " doesn't exist")
			return False, {'CANCELLED'}

		if self.with_add_bones == False:
			while len(self.add_bones) != 0:
				self.add_bones.remove(0)

		for bone in self.add_bones:
			if bone.name_FK not in context.active_object.data.bones.keys():
				self.report({'ERROR'}, "Bone " + bone.name_FK + " doesn't exist")
				return False, {'CANCELLED'}
			if bone.name_IK not in context.active_object.data.bones.keys():
				self.report({'ERROR'}, "Bone " + bone.name_IK + " doesn't exist")
				return False, {'CANCELLED'}

		return True, True


	def fk2ik_check(self, context):
		if self.with_stay_bones == False:
			while len(self.stay_bones) != 0:
				self.stay_bones.remove(0)

		for bone in self.stay_bones:
			if bone.name not in context.active_object.data.bones.keys():
				self.report({'ERROR'}, "Bone " + bone.name + " doesn't exist")
				return False, {'CANCELLED'}

		if self.with_roll_bones == True:
			if self.ik_mech_foot == "":
				self.report({'ERROR'}, "Mech foot must be filled")
				return False, {'CANCELLED'}
			else:
				if self.ik_mech_foot not in context.active_object.data.bones.keys():
					self.report({'ERROR'}, "Bone " + self.ik_mech_foot + " doesn't exist")
					return False, {'CANCELLED'}

		return True, True


	def ik2fk_check(self, context):
		if self.ik_type == "POLE" and self.ik4 == "":
			self.report({'ERROR'}, "IK pole must be filled")
			return False, {'CANCELLED'}

		#if snap is set to "POLE", check that bone ik2 has really an IK constraint with a pole
		if self.ik_type == "POLE":
			ik = context.active_object.pose.bones[self.ik2]
			for constr in ik.constraints:
				if constr.type == "IK":
					if constr.pole_subtarget == "":
						self.report({'ERROR'}, "IK constraint must have a pole target bone")
						return False, {'CANCELLED'}

		if self.ik_type == "ROTATION": #No pole if IK type is set to rotation
			self.ik4 = ""

		if self.with_roll_bones == False:
			while len(self.roll_bones) != 0:
				self.roll_bones.remove(0)

		if self.ik4 != "" and self.ik4 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik4 + " doesn't exist")
			return False, {'CANCELLED'}

		for bone in self.roll_bones:
			if bone.name not in context.active_object.data.bones.keys():
				self.report({'ERROR'}, "Bone " + bone.name + " doesn't exist")
				return False, {'CANCELLED'}

		return True, True

	def interaction_check(self, context):
		if self.autoswitch == True:
			try:
				int(context.active_object.pose.bones[self.autoswitch_data_bone].get(self.autoswitch_data_property))
				return True, True
			except:
				self.report({'ERROR'}, "Wrong Bone property (AutoSwitch)")
				return False, {'CANCELLED'}

		if self.autodisplay == True and self.autodisplay_data_type == "HIDE":
			try:
				int(context.active_object.pose.bones[self.autodisplay_data_bone].get(self.autodisplay_data_property))
				return True, True
			except:
				self.report({'ERROR'}, "Wrong Bone property (AutoDisplay)")
				return False, {'CANCELLED'}

		if self.autokeyframe == True and self.autokeyframe_data_type == "KEYING_SET":
			if self.autokeyframe_data_keying_set_FK == "":
				self.report({'ERROR'}, "FK Keying Set must be filled")
				return False, {'CANCELLED'}
			if self.autokeyframe_data_keying_set_IK == "":
				self.report({'ERROR'}, "IK Keying Set must be filled")
				return False, {'CANCELLED'}
		if self.autokeyframe == True and self.autokeyframe_data_type == "AVAILABLE":
			if self.check_available_curve(self.get_list_bones(context)) == False:
				self.report({'ERROR'}, "No Available Keyframes")
				return False, {'CANCELLED'}

		return True, True

	def execute(self, context):

		status, error = self.layout_check(context, self.layout_basic)
		if status == False:
			return error

		#No interaction for basic layout
		if self.layout_basic == False:
			status, error = self.interaction_check(context)
			if status == False:
				return error

		way = ""
		if self.layout_basic == True and self.switch_way == "FK2IK":
			way = "FK2IK"
		elif self.layout_basic == True and self.switch_way == "IK2FK":
			way = "IK2FK"
		elif self.layout_basic == False and int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property)) == 1.0 and self.switch_invert == "IKIS0":
			way = "IK2FK"
		elif self.layout_basic == False and int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property)) == 1.0 and self.switch_invert == "FKIS0":
			way = "FK2IK"
		elif self.layout_basic == False and int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property)) == 0.0 and self.switch_invert == "IKIS0":
			way = "FK2IK"
		elif self.layout_basic == False and int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property)) == 0.0 and self.switch_invert == "FKIS0":
			way = "IK2FK"

		status, error = self.common_check(context)
		if status == False:
			return error

		if way == "IK2FK":
			status, error = self.ik2fk_check(context)
			if status == False:
				return error
		elif way == "FK2IK":
			status, error = self.fk2ik_check(context)
			if status == False:
				return error

		if way == "IK2FK":
			self.ik2fk(context.active_object, self.root, self.ik1, self.ik2, self.ik3, self.ik4, self.ik5, self.fk1, self.fk2, self.fk3, self.fk4, self.ik_scale, self.fk_scale, self.ik_location, self.fk_location, self.roll_bones, self.add_bones)
		elif way == "FK2IK":
			self.fk2ik(context.active_object, self.root, self.ik1, self.ik2, self.ik3, self.ik5, self.ik_scale, self.ik_location,  self.fk1, self.fk2, self.fk3, self.fk4, self.fk_scale, self.fk_location, self.add_bones, self.ik_mech_foot, self.stay_bones)

		if self.layout_basic == False: #No interaction for basic layout
			#AutoSwitch
			if self.layout_basic == False and self.autoswitch == True:
				if int(context.active_object.pose.bones[self.autoswitch_data_bone].get(self.autoswitch_data_property)) == 0:
					context.active_object.pose.bones[self.autoswitch_data_bone][self.autoswitch_data_property] = 1.0
				else:
					context.active_object.pose.bones[self.autoswitch_data_bone][self.autoswitch_data_property] = 0.0
				#AutoSwitch Keyframe
				if self.autoswitch_keyframe == True:
					context.active_object.pose.bones[self.autoswitch_data_bone].keyframe_insert("[\"" + self.autoswitch_data_property + "\"]")
					#change interpolation
					curves = context.active_object.animation_data.action.fcurves
					for c in curves:
						if c.data_path == 'pose.bones["' + self.autoswitch_data_bone + '"][\"' + self.autoswitch_data_property + '\"]':
							curve = c
							break
					current_frame = bpy.context.scene.frame_current
					cpt = 0
					for point in curve.keyframe_points:
						if point.co[0] == current_frame:
							if cpt != 0:
								curve.keyframe_points[cpt-1].interpolation = 'CONSTANT'
								break
							else:
								break
						cpt = cpt + 1

			#AutoDisplay
			if self.autodisplay == True:
				if self.autodisplay_data_type == "LAYER":
					if way == "FK2IK":
						#Display FK layers, and the hide IK layers
						cpt = 0
						for layer in self.autodisplay_data_layer_fk:
							if layer == True:
								context.active_object.data.layers[cpt] = True
							cpt = cpt + 1
						cpt = 0
						for layer in self.autodisplay_data_layer_ik:
							if layer == True:
								context.active_object.data.layers[cpt] = False
							cpt = cpt + 1
					elif way == "IK2FK":
						#Display IK layers, and the hide FK layers
						cpt = 0
						for layer in self.autodisplay_data_layer_ik:
							if layer == True:
								context.active_object.data.layers[cpt] = True
							cpt = cpt + 1
						cpt = 0
						for layer in self.autodisplay_data_layer_fk:
							if layer == True:
								context.active_object.data.layers[cpt] = False
							cpt = cpt + 1
				elif self.autodisplay_data_type == "HIDE":
					if int(context.active_object.pose.bones[self.autodisplay_data_bone].get(self.autodisplay_data_property)) == 0 and self.autodisplay_data_invert == False:
						context.active_object.pose.bones[self.autodisplay_data_bone][self.autodisplay_data_property] = 1.0
					elif int(context.active_object.pose.bones[self.autodisplay_data_bone].get(self.autodisplay_data_property)) == 0 and self.autodisplay_data_invert == True:
						context.active_object.pose.bones[self.autodisplay_data_bone][self.autodisplay_data_property] = 0.0
					elif int(context.active_object.pose.bones[self.autodisplay_data_bone].get(self.autodisplay_data_property)) == 1 and self.autodisplay_data_invert == False:
						context.active_object.pose.bones[self.autodisplay_data_bone][self.autodisplay_data_property] = 0.0
					elif int(context.active_object.pose.bones[self.autodisplay_data_bone].get(self.autodisplay_data_property)) == 1 and self.autodisplay_data_invert == True:
						context.active_object.pose.bones[self.autodisplay_data_bone][self.autodisplay_data_property] = 1.0

			if self.autokeyframe == True:
				if self.autokeyframe_data_type == "KEYING_SET":
					#store current keying set used
					current_keying_set = context.scene.keying_sets.active_index
					#Set keying_set to FK keying_set
					context.scene.keying_sets.active_index = context.scene.keying_sets.find(self.autokeyframe_data_keying_set_FK)
					#Insert Keyframe
					bpy.ops.anim.keyframe_insert_menu(type='__ACTIVE__')
					#Set keying_set to IK keying_set
					context.scene.keying_sets.active_index = context.scene.keying_sets.find(self.autokeyframe_data_keying_set_IK)
					#Insert Keyframe
					bpy.ops.anim.keyframe_insert_menu(type='__ACTIVE__')
					#Retrieve current keying set
					context.scene.keying_sets.active_index = current_keying_set
				elif self.autokeyframe_data_type == "AVAILABLE":
					#store current keying set used
					current_keying_set = context.scene.keying_sets.active_index
					#set keying_set to available
					bpy.context.scene.keying_sets.active = bpy.context.scene.keying_sets_all['Available']
					# Construct override context
					override = bpy.context.copy()
					override['selected_pose_bones'] = self.get_list_bones(context)
					#Insert Keyframe
					bpy.ops.anim.keyframe_insert(override)
					#Retrieve current keying set
					context.scene.keying_sets.active_index = current_keying_set

		return {'FINISHED'}

	def get_list_bones(self, context):
		list_ = []
		if self.root != "" and self.root in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.root])
		if self.ik1 != "" and self.ik1 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.ik1])
		if self.ik2 != "" and self.ik2 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.ik2])
		if self.ik3 != "" and self.ik3 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.ik3])
		if self.ik4 != "" and self.ik4 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.ik4])
		if self.ik5 != "" and self.ik5 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.ik5])
		if self.ik_scale != "" and self.ik_scale in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.ik_scale])
		if self.ik_location != "" and self.ik_location in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.ik_location])
		if self.ik_mech_foot != "" and self.ik_mech_foot in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.ik_mech_foot])
		if self.fk1 != "" and self.fk1 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.fk1])
		if self.fk2 != "" and self.fk2 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.fk2])
		if self.fk3 != "" and self.fk3 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.fk3])
		if self.fk4 != "" and self.fk4 in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.fk4])
		if self.fk_scale != "" and self.fk_scale in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.fk_scale])
		if self.fk_location != "" and self.fk_location in context.active_object.data.bones.keys():
			list_.append(context.active_object.pose.bones[self.fk_location])

		for bone in self.roll_bones:
			if bone.name != "" and bone.name in context.active_object.data.bones.keys():
				list_.append(context.active_object.pose.bones[bone.name])

		for bone in self.stay_bones:
			if bone.name != "" and bone.name in context.active_object.data.bones.keys():
				list_.append(context.active_object.pose.bones[bone.name])

		for bone in self.add_bones:
			if bone.name_FK != "" and bone.name_FK in context.active_object.data.bones.keys():
				list_.append(context.active_object.pose.bones[bone.name_FK])
			if bone.name_IK != "" and bone.name_IK in context.active_object.data.bones.keys():
				list_.append(context.active_object.pose.bones[bone.name_IK])

		return list_

	def perpendicular(self, v):
		if v != mathutils.Vector((1,1,1)):
			other = mathutils.Vector((1,0,0))
		else:
			other = mathutils.Vector((0,1,0))
		return v.cross(other)

	def set_position(self, obj,ref,pole,pos):
		mat_loc = mathutils.Matrix.Translation(pos)
		mat = obj.convert_space(pole,obj.convert_space(ref, mat_loc,'POSE','WORLD'), 'WORLD','LOCAL')
		pole.location = mat.to_translation()
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

	def rotation_diff(self, mat1,mat2):
		quat1 = mat1.to_quaternion()
		quat2 = mat2.to_quaternion()
		angle = math.acos(min(1,max(-1,quat1.dot(quat2)))) * 2
		if angle > math.pi:
			angle = -angle + 2*math.pi
		return angle

	def ik2fk(self, obj, root_, ik1_, ik2_, ik3_, ik4_, ik5_, fk1_, fk2_, fk3_, fk4_, ik_scale_, fk_scale_, ik_location_, fk_location_, roll_bones, add_bones):
		ik1 = obj.pose.bones[ik1_]
		ik2 = obj.pose.bones[ik2_]
		ik3 = obj.pose.bones[ik3_]
		if ik4_ != "":
			ik4 = obj.pose.bones[ik4_]
		if ik5_ != "":
			ik5 = obj.pose.bones[ik5_]
		fk1 = obj.pose.bones[fk1_]
		fk2 = obj.pose.bones[fk2_]
		fk3 = obj.pose.bones[fk3_]
		if fk4_ != "":
			fk4 = obj.pose.bones[fk4_]
		if ik_scale_ != "":
			ik_scale = obj.pose.bones[ik_scale_]

		if fk_scale_ != "":
			fk_scale = obj.pose.bones[fk_scale_]

		if root_ != "":
			root = obj.pose.bones[root_]
			root_scale_data = root.scale
		else:
			root_scale_data = mathutils.Vector((1.0,1.0,1.0))
		if ik_location_ != "":
			ik_location = obj.pose.bones[ik_location_]
		if fk_location_ != "":
			fk_location = obj.pose.bones[fk_location_]

		if ik_scale_ != "" and fk_scale_ != "":
			ik_scale.scale = fk_scale.scale
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		if ik_scale_ != "" and fk_scale_ == "":
			ik_scale.scale = mathutils.Vector((1.0,1.0,1.0))
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		if fk_scale_ != "" and ik_scale_ == "":
			fk_scale.scale = mathutils.Vector((1.0,1.0,1.0))
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		if ik_scale_ != "":
			ik_scale_data = ik_scale.scale
		else:
			ik_scale_data = mathutils.Vector((1.0,1.0,1.0))

		if fk_scale_ != "":
			fk_scale_data = fk_scale.scale
		else:
			fk_scale_data = mathutils.Vector((1.0,1.0,1.0))

		if ik_location_ != "" and fk_location_ != "":
			ik_location.location = obj.convert_space(ik_location, obj.convert_space(fk_location, fk_location.matrix_basis,'POSE','WORLD'), 'WORLD','POSE').to_translation()
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		if ik_location_ != "" and fk_location_ == "":
			ik_location.location = mathutils.Vector((0.0,0.0,0.0))
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		for bone in roll_bones:
			obj.pose.bones[bone.name].matrix_basis = mathutils.Matrix()

		for b_FK, b_IK in [[bone.name_FK, bone.name_IK] for bone in add_bones]:
			obj.pose.bones[b_IK].matrix = obj.pose.bones[b_FK].matrix
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

		ik3.matrix = obj.convert_space(ik3, obj.convert_space(fk3, fk3.matrix,'POSE','WORLD'), 'WORLD','POSE') * ( fk3.bone.matrix_local.inverted() * ik3.bone.matrix_local )
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

		if ik4_ != "":
			if ik_scale_ != "":
				distance = ik_scale.scale.y
			else:
				distance = 1.0

		ik1.matrix = obj.convert_space(ik1, obj.convert_space(fk1, fk1.matrix, 'POSE', 'WORLD'), 'WORLD','POSE') #for translation
		ik1.scale = obj.convert_space(ik1, obj.convert_space(fk1, fk1.matrix, 'POSE', 'WORLD'), 'WORLD','POSE').to_scale()
		ik1.scale.x = ik1.scale.x / ik_scale_data[0] / root_scale_data[0]
		ik1.scale.y = ik1.scale.y / ik_scale_data[1] / root_scale_data[1]
		ik1.scale.z = ik1.scale.z / ik_scale_data[2] / root_scale_data[2]
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')
		if obj.data.bones[ik2_].use_inherit_scale == True:
			ik2.scale = obj.convert_space(ik2, obj.convert_space(fk2, fk2.matrix, 'POSE', 'WORLD'), 'WORLD','POSE').to_scale()
			ik2.scale.x = ik2.scale.x / ik1.scale.x / ik_scale_data[0] / root_scale_data[0]
			ik2.scale.y = ik2.scale.y / ik1.scale.y / ik_scale_data[1] / root_scale_data[1]
			ik2.scale.z = ik2.scale.z / ik1.scale.z / ik_scale_data[2] / root_scale_data[2]
		else:
			ik2.scale = obj.convert_space(ik2, obj.convert_space(fk2, fk2.matrix, 'POSE', 'WORLD'), 'WORLD','POSE').to_scale()
			ik2.scale.x = ik2.scale.x / ik_scale_data[0] / root_scale_data[0]
			ik2.scale.y = ik2.scale.y / ik_scale_data[1] / root_scale_data[1]
			ik2.scale.z = ik2.scale.z / ik_scale_data[2] / root_scale_data[2]
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

		fk2_current_rotation_mode = fk2.rotation_mode
		ik2_current_rotation_mode = ik2.rotation_mode
		fk2.rotation_mode = 'QUATERNION'
		ik2.rotation_mode = 'QUATERNION'
		ik2.rotation_quaternion = fk2.rotation_quaternion
		fk2.rotation_mode = fk2_current_rotation_mode
		ik2.rotation_mode = ik2_current_rotation_mode
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

		if ik4_ != "":
			limb	  = ik2.matrix.to_translation() + ik2.vector - ik1.matrix.to_translation()
			perp_limb = self.perpendicular(limb).normalized() * distance

			loc = ik1.matrix.to_translation() + limb/2 + perp_limb
			self.set_position(obj,ik1,ik4,loc)

			angle = self.rotation_diff(ik1.matrix, fk1.matrix)

			perp_v1 = mathutils.Matrix.Rotation(angle, 4, limb) * perp_limb
			loc1 = ik1.matrix.to_translation() + limb/2 + perp_v1
			self.set_position(obj, ik1, ik4, loc1)
			angle1 = self.rotation_diff(ik1.matrix, fk1.matrix)

			perp_v2 = mathutils.Matrix.Rotation(-angle, 4, limb) * perp_limb
			loc2 = ik1.matrix.to_translation() + limb/2 + perp_v2
			self.set_position(obj, ik1, ik4, loc2)
			angle2 = self.rotation_diff(ik1.matrix, fk1.matrix)

			if angle1 < angle2:
				self.set_position(obj, ik1, ik4, loc1)

		if fk4_ != "" and ik5_ != "":
			fk4_current_rotation_mode = fk4.rotation_mode
			ik5_current_rotation_mode = ik5.rotation_mode
			fk4.rotation_mode = 'QUATERNION'
			ik5.rotation_mode = 'QUATERNION'
			ik5.matrix = obj.convert_space(ik5, obj.convert_space(fk4, fk4.matrix,'POSE','WORLD'), 'WORLD','POSE')
			fk4.rotation_mode = fk4_current_rotation_mode
			ik5.rotation_mode = ik5_current_rotation_mode
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

	def fk2ik(self, obj, root_, ik1_, ik2_, ik3_, ik5_, ik_scale_, ik_location_, fk1_, fk2_, fk3_, fk4_, fk_scale_, fk_location_, add_bones, ik_mech_foot_, stay_bones):
		ik1 = obj.pose.bones[ik1_]
		ik2 = obj.pose.bones[ik2_]
		ik3 = obj.pose.bones[ik3_]
		if ik5_ != "":
			ik5 = obj.pose.bones[ik5_]
		if ik_mech_foot_ != "":
			ik_mech_foot = obj.pose.bones[ik_mech_foot_]
		fk1 = obj.pose.bones[fk1_]
		fk2 = obj.pose.bones[fk2_]
		fk3 = obj.pose.bones[fk3_]
		if fk4_ != "":
			fk4 = obj.pose.bones[fk4_]
		if ik_scale_ != "":
			ik_scale = obj.pose.bones[ik_scale_]
		if fk_scale_ != "":
			fk_scale = obj.pose.bones[fk_scale_]
		if root_ != "":
			root = obj.pose.bones[root_]

		if ik_scale_ != "" and fk_scale_ != "":
			fk_scale.scale = ik_scale.scale
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		if ik_scale_ != "" and fk_scale_ == "":
			ik_scale.scale = mathutils.Vector((1.0,1.0,1.0))
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		if fk_scale_ != "" and ik_scale_ == "":
			fk_scale.scale = mathutils.Vector((1.0,1.0,1.0))
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		if ik_scale_ != "":
			ik_scale_data = ik_scale.scale
		else:
			ik_scale_data = mathutils.Vector((1.0,1.0,1.0))

		if fk_scale_ != "":
			fk_scale_data = fk_scale.scale
		else:
			fk_scale_data = mathutils.Vector((1.0,1.0,1.0))

		if ik_location_ != "":
			ik_location = obj.pose.bones[ik_location_]
		if fk_location_ != "":
			fk_location = obj.pose.bones[fk_location_]

		if ik_location_ != "" and fk_location_ != "":
			fk_location.location = obj.convert_space(fk_location, obj.convert_space(ik_location, ik_location.matrix_basis,'POSE','WORLD'), 'WORLD','POSE').to_translation()
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		if fk_location_ != "" and ik_location_ == "":
			fk_location.location = mathutils.Vector((0.0,0.0,0.0))
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		fk1_current_rotation_mode = fk1.rotation_mode
		ik1_current_rotation_mode = ik1.rotation_mode
		fk1.rotation_mode = 'QUATERNION'
		ik1.rotation_mode = 'QUATERNION'
		fk1.matrix = obj.convert_space(fk1, obj.convert_space(ik1, ik1.matrix,'POSE','WORLD'), 'WORLD','POSE')
		fk1.rotation_mode = fk1_current_rotation_mode
		ik1.rotation_mode = ik1_current_rotation_mode
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

		fk2_current_rotation_mode = fk2.rotation_mode
		ik2_current_rotation_mode = ik2.rotation_mode
		fk2.rotation_mode = 'QUATERNION'
		ik2.rotation_mode = 'QUATERNION'
		fk2.matrix = obj.convert_space(fk2, obj.convert_space(ik2, ik2.matrix,'POSE','WORLD'), 'WORLD','POSE')
		fk2.rotation_mode = fk2_current_rotation_mode
		ik2.rotation_mode = ik2_current_rotation_mode
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

		for bone in stay_bones:
			obj.pose.bones[bone.name].matrix = obj.pose.bones[bone.name].matrix.inverted() * (obj.convert_space(fk3, obj.convert_space(ik_mech_foot, ik_mech_foot.matrix,'POSE','WORLD'), 'WORLD','POSE') * ( ik_mech_foot.bone.matrix_local.inverted() * ik3.bone.matrix_local) * ( ik3.bone.matrix_local.inverted() * fk3.bone.matrix_local ) * (ik3.matrix.inverted() * fk3.matrix)).inverted() * fk3.matrix
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

		fk3_current_rotation_mode = fk3.rotation_mode
		ik3_current_rotation_mode = ik3.rotation_mode
		fk3.rotation_mode = 'QUATERNION'
		ik3.rotation_mode = 'QUATERNION'
		fk3.matrix = obj.convert_space(fk3, obj.convert_space(ik_mech_foot, ik_mech_foot.matrix,'POSE','WORLD'), 'WORLD','POSE') * ( ik_mech_foot.bone.matrix_local.inverted() * ik3.bone.matrix_local) * ( ik3.bone.matrix_local.inverted() * fk3.bone.matrix_local )
		fk3.rotation_mode = fk3_current_rotation_mode
		ik3.rotation_mode = ik3_current_rotation_mode
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')

		if fk4_ != "" and ik5_ != "":
			fk4_current_rotation_mode = fk4.rotation_mode
			ik5_current_rotation_mode = ik5.rotation_mode
			fk4.rotation_mode = 'QUATERNION'
			ik5.rotation_mode = 'QUATERNION'
			fk4.matrix = obj.convert_space(fk4, obj.convert_space(ik5, ik5.matrix,'POSE','WORLD'), 'WORLD','POSE')
			fk4.rotation_mode = fk4_current_rotation_mode
			ik5.rotation_mode = ik5_current_rotation_mode
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.mode_set(mode='POSE')

		for b_FK, b_IK in [[bone.name_FK, bone.name_IK] for bone in add_bones]:
			obj.pose.bones[b_FK].matrix = obj.pose.bones[b_IK].matrix
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.mode_set(mode='POSE')


class POSE_OT_juas_generate_snapping(bpy.types.Operator):
	"""Generate snapping"""
	bl_idname = "pose.juas_generate_snapping"
	bl_label = "Generate Snapping"
	bl_options = {'REGISTER'}


	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.juas_limbs) > 0 and context.mode == 'POSE'

	def execute(self, context):

		if context.active_object.juas_generation.panel_name == "":
			context.active_object.juas_generation.panel_name = addonpref().panel_name
		if context.active_object.juas_generation.tab_tool == "":
			context.active_object.juas_generation.tab_tool = addonpref().tab_tool

		#Add rig_id custom prop if not exists, and assign a random value
		if context.active_object.data.get('autosnap_rig_id') is None:
			bpy.context.active_object.data['autosnap_rig_id'] = uuid.uuid4().hex
		rig_id = context.active_object.data.get('autosnap_rig_id')

		#retrieve FK/IK switch source code
		source, lines = inspect.getsourcelines(getattr(bpy.types, bpy.ops.pose.juas_limb_switch_ikfk.idname()))
		source[0] = source[0].replace(bpy.ops.pose.juas_limb_switch_ikfk.idname(), bpy.ops.pose.juas_limb_switch_ikfk.idname() + "_" + rig_id)
		source[2] = source[2].replace("pose.juas_limb_switch_ikfk", "pose.juas_limb_switch_ikfk_" + rig_id)

		generated_text_ops_ = generated_text_ops
		generated_text_ops_ = generated_text_ops_.replace("###rig_id###", rig_id )
		generated_text_ops_ = generated_text_ops_.replace("###CLASS_switch_FKIK###", "".join(source))
		generated_text_ops_ = generated_text_ops_.replace("###CLASS_switch_FKIK_name###", bpy.ops.pose.juas_limb_switch_ikfk.idname() + "_" + rig_id)

		if context.active_object.data["autosnap_rig_id"] + "_autosnap_ops.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[context.active_object.data["autosnap_rig_id"] + "_autosnap_ops.py"])
		text = bpy.data.texts.new(name=context.active_object.data["autosnap_rig_id"] + "_autosnap_ops.py")
		text.use_module = True
		text.write(generated_text_ops_)
		exec(text.as_string(), {})

		#Generate ui text
		ui_generated_text_ = ui_generated_text
		ui_generated_text_ = ui_generated_text_.replace("###LABEL###", context.active_object.juas_generation.panel_name)
		ui_generated_text_ = ui_generated_text_.replace("###REGION_TYPE###", context.active_object.juas_generation.view_location)
		ui_generated_text_ = ui_generated_text_.replace("###CATEGORY###", context.active_object.juas_generation.tab_tool)
		ui_generated_text_ = ui_generated_text_.replace("###rig_id###", rig_id )

		total_layout_ = ""
		for limb in context.active_object.juas_limbs:
			if limb.layout.on_select == True:
				tabs = "\t\t\t"
				ui_layout_on_select_ = ui_layout_on_select.replace("###ON_SELECT_TAB###", str([bone.name for bone in limb.select_bones]))
				ui_layout_on_select_ = ui_layout_on_select_.replace("###tab_minus###", "\t\t")
			else:
				tabs = "\t\t"

			if limb.layout.basic == True:

				if limb.layout.on_select == False:
					ui_layout_basic_ = ui_layout_basic.replace("###ON_SELECT###", "")
				else:
					ui_layout_basic_ = ui_layout_basic.replace("###ON_SELECT###", ui_layout_on_select_)

				ui_generated_switch_param_ = ui_generated_switch_param
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###tab###",tabs)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###root###", limb.root)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_type###", limb.ik_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###global_scale###", str(limb.global_scale))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_scale_type###", limb.ik_scale_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_scale_type###", limb.fk_scale_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_location_type###", limb.ik_location_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_location_type###", limb.fk_location_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###with_limb_end_fk###", str(limb.with_limb_end_fk))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###with_limb_end_ik###", str(limb.with_limb_end_ik))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik1###", limb.ik1)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik2###", limb.ik2)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik3###", limb.ik3)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik4###", limb.ik4)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik5###", limb.ik5)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_mech_foot###", limb.ik_mech_foot)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk1###", limb.fk1)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk2###", limb.fk2)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk3###", limb.fk3)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk4###", limb.fk4)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_scale###", limb.ik_scale)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_scale###", limb.fk_scale)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_location###", limb.ik_location)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_location###", limb.fk_location)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###WITH_ROLL_BONES###", str(limb.with_roll_bones))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###WITH_STAY_BONES###", str(limb.with_stay_bones))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###WITH_ADD_BONES###", str(limb.with_add_bones))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###limb_roll_bones###", str([bone.name for bone in limb.roll_bones]))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###limb_stay_bones###", str([bone.name for bone in limb.stay_bones]))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###limb_add_bones###", str([[bone.name_FK, bone.name_IK] for bone in limb.add_bones]))

				if limb.layout.display_name == True:
					ui_layout_basic_limb_name_ = ui_layout_basic_limb_name.replace("###limb###", limb.name)
					ui_layout_basic_limb_name_ = ui_layout_basic_limb_name_.replace("###tab###", tabs)
					ui_layout_basic_ = ui_layout_basic_.replace("###LIMB_NAME###", ui_layout_basic_limb_name_)

				else:
					ui_layout_basic_ = ui_layout_basic_.replace("###LIMB_NAME###", "")

				ui_layout_basic_ = ui_layout_basic_.replace("###FK2IK_LABEL###", limb.layout.fk2ik_label)
				ui_layout_basic_ = ui_layout_basic_.replace("###IK2FK_LABEL###", limb.layout.ik2fk_label)
				ui_layout_basic_ = ui_layout_basic_.replace("###rig_id###", rig_id)
				ui_layout_basic_ = ui_layout_basic_.replace("###GENERATED_bone_PARAM###",ui_generated_switch_param_)
				ui_layout_basic_ = ui_layout_basic_.replace("###tab###", tabs)

				total_layout_ = total_layout_ + ui_layout_basic_

			else:

				if limb.layout.on_select == False:
					ui_layout_non_basic_ = ui_layout_non_basic.replace("###ON_SELECT###", "")
				else:
					ui_layout_non_basic_ = ui_layout_non_basic.replace("###ON_SELECT###", ui_layout_on_select_)

				ui_generated_switch_param_ = ui_generated_switch_param
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###tab###",tabs)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###root###", limb.root)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_type###", limb.ik_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###global_scale###", str(limb.global_scale))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_scale_type###", limb.ik_scale_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_scale_type###", limb.fk_scale_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_location_type###", limb.ik_location_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_location_type###", limb.fk_location_type)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###with_limb_end_fk###", str(limb.with_limb_end_fk))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###with_limb_end_ik###", str(limb.with_limb_end_ik))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik1###", limb.ik1)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik2###", limb.ik2)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik3###", limb.ik3)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik4###", limb.ik4)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik5###", limb.ik5)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_mech_foot###", limb.ik_mech_foot)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk1###", limb.fk1)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk2###", limb.fk2)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk3###", limb.fk3)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk4###", limb.fk4)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_scale###", limb.ik_scale)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_scale###", limb.fk_scale)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_location###", limb.ik_location)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_location###", limb.fk_location)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###WITH_ROLL_BONES###", str(limb.with_roll_bones))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###WITH_STAY_BONES###", str(limb.with_stay_bones))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###WITH_ADD_BONES###", str(limb.with_add_bones))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###limb_roll_bones###", str([bone.name for bone in limb.roll_bones]))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###limb_stay_bones###", str([bone.name for bone in limb.stay_bones]))
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###limb_add_bones###", str([[bone.name_FK, bone.name_IK] for bone in limb.add_bones]))

				if limb.layout.display_name == True:
					ui_layout_non_basic_limb_name_ = ui_layout_non_basic_limb_name.replace("###tab###",tabs)
					ui_layout_non_basic_limb_name_ = ui_layout_non_basic_limb_name_.replace("###limb###", limb.name)
					ui_layout_non_basic_ = ui_layout_non_basic_.replace("###LIMB_NAME###", ui_layout_non_basic_limb_name_)
				else:
					ui_layout_non_basic_ = ui_layout_non_basic.replace("###LIMB_NAME###", "")

				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###FK2IK_LABEL###", limb.layout.fk2ik_label)
				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###IK2FK_LABEL###", limb.layout.ik2fk_label)
				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###rig_id###", rig_id)
				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_bone_PARAM###",ui_generated_switch_param_)
				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###SWITCH_BONE###",limb.layout.switch_bone)
				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###SWITCH_PROPERTY###",limb.layout.switch_property)
				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###SWITCH_INVERT###",limb.layout.switch_invert)

				if limb.interaction.autoswitch == True:
					#create properties and set to False by default
					bpy.types.PoseBone.autosnap_autoswitch = bpy.props.BoolProperty(name="AutoSwitch")
					bpy.types.PoseBone.autosnap_autoswitch_keyframe = bpy.props.BoolProperty(name="AutoSwitch Keyframe")
					if limb.interaction.bone_store != "":
						bpy.context.active_object.pose.bones[limb.interaction.bone_store].autosnap_autoswitch = False
						bpy.context.active_object.pose.bones[limb.interaction.bone_store].autosnap_autoswitch_keyframe = False

				if limb.interaction.autodisplay == True:
					#create properties and set to False by default
					bpy.types.PoseBone.autosnap_autodisplay = bpy.props.BoolProperty(name="AutoDisplay")
					if limb.interaction.bone_store != "":
						bpy.context.active_object.pose.bones[limb.interaction.bone_store].autosnap_autodisplay = False

				#AutoSwitch : Param
				if limb.interaction.autoswitch_data.bone != "" and limb.interaction.bone_store != "":
					ui_autoswitch_param_ = ui_autoswitch_param.replace("###AUTOSWITCH_BONE###", limb.interaction.autoswitch_data.bone)
					ui_autoswitch_param_ = ui_autoswitch_param_.replace("###AUTOSWITCH_BONE_STORE###", limb.interaction.bone_store)
					ui_autoswitch_param_ = ui_autoswitch_param_.replace("###AUTOSWITCH_PROPERTY###", limb.interaction.autoswitch_data.property)
					ui_autoswitch_param_ = ui_autoswitch_param_.replace("###tab###", tabs)
				else:
					ui_autoswitch_param_ = ui_autoswitch_param_ko
					ui_autoswitch_param_ = ui_autoswitch_param_.replace("###tab###", tabs)

				#AutoDisplay : Param
				if limb.interaction.bone_store != "":
					ui_autodisplay_param_ = ui_autodisplay_param.replace("###AUTODISPLAY_BONE_STORE###", limb.interaction.bone_store)
					ui_autodisplay_param_ = ui_autodisplay_param_.replace("###AUTODISPLAY_TYPE###", limb.interaction.autodisplay_data.type)
					if limb.interaction.autodisplay_data.type == "LAYER":
						ui_autodisplay_param_layer_ = ui_autodisplay_param_layer.replace("###AUTODISPLAY_LAYER_IK###", str([layer for layer in limb.interaction.autodisplay_data.layer_ik]))
						ui_autodisplay_param_layer_ = ui_autodisplay_param_layer_.replace("###AUTODISPLAY_LAYER_FK###", str([layer for layer in limb.interaction.autodisplay_data.layer_fk]))
						ui_autodisplay_param_ = ui_autodisplay_param_.replace("###AUTODISPLAY_PARAM_TYPE###", ui_autodisplay_param_layer_)
					elif limb.interaction.autodisplay_data.type == "HIDE":
						ui_autodisplay_param_hide_ = ui_autodisplay_param_hide.replace("###AUTODISPLAY_BONE###", limb.interaction.autodisplay_data.bone)
						ui_autodisplay_param_hide_ = ui_autodisplay_param_hide_.replace("###AUTODISPLAY_PROPERTY###", limb.interaction.autodisplay_data.property)
						ui_autodisplay_param_hide_ = ui_autodisplay_param_hide_.replace("###AUTODISPLAY_INVERT###", str(limb.interaction.autodisplay_data.invert))
						ui_autodisplay_param_ = ui_autodisplay_param_.replace("###AUTODISPLAY_PARAM_TYPE###", ui_autodisplay_param_hide_)
					ui_autodisplay_param_ = ui_autodisplay_param_.replace("###tab###", tabs)
				else:
					ui_autodisplay_param_ = ui_autodisplay_param_ko
					ui_autodisplay_param_ = ui_autodisplay_param_.replace("###tab###", tabs)

				#AutoKeyframe : Create properties
				if limb.interaction.autokeyframe == True:
					bpy.types.PoseBone.autosnap_autokeyframe = bpy.props.BoolProperty(name="AutoKeyframe")
					if limb.interaction.bone_store != "":
						bpy.context.active_object.pose.bones[limb.interaction.bone_store].autosnap_autokeyframe = False

				#AutoKeyframe : Param
				if limb.interaction.bone_store != "":
					ui_autokeyframe_param_ = ui_autokeyframe_param.replace("###AUTOKEYFRAME_BONE_STORE###", limb.interaction.bone_store)
					ui_autokeyframe_param_ = ui_autokeyframe_param_.replace("###AUTOKEYFRAME_TYPE###", limb.interaction.autokeyframe_data.type)
					if limb.interaction.autokeyframe_data.type == "AVAILABLE":
						ui_autokeyframe_param_ = ui_autokeyframe_param_.replace("###AUTOKEYFRAME_PARAM###","")
						ui_autokeyframe_param_ = ui_autokeyframe_param_.replace("###tab###", tabs)
					elif limb.interaction.autokeyframe_data.type == "KEYING_SET":
						ui_autokeyframe_param_keyingset_ = ui_autokeyframe_param_keyingset.replace("###AUTOKEYFRAME_KEYING_SET_FK###",limb.interaction.autokeyframe_data.keying_set_FK)
						ui_autokeyframe_param_keyingset_ = ui_autokeyframe_param_keyingset_.replace("###AUTOKEYFRAME_KEYING_SET_IK###",limb.interaction.autokeyframe_data.keying_set_IK)
						ui_autokeyframe_param_ = ui_autokeyframe_param_.replace("###AUTOKEYFRAME_PARAM###", ui_autokeyframe_param_keyingset_)
						ui_autokeyframe_param_ = ui_autokeyframe_param_.replace("###tab###", tabs)

				else:
					ui_autokeyframe_param_ = ui_autokeyframe_param_ko
					ui_autokeyframe_param_ = ui_autokeyframe_param_.replace("###tab###", tabs)


				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autoswitch_PARAM###",ui_autoswitch_param_)
				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autodisplay_PARAM###",ui_autodisplay_param_)
				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autokeyframe_PARAM###",ui_autokeyframe_param_)

				#autoswitch : UI
				if limb.interaction.autoswitch == False:
					ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autoswitch_UI###","")
				else:
					ui_layout_non_basic_autoswitch_ = ui_layout_non_basic_autoswitch.replace("###SWITCH_BONE_STORE###",limb.interaction.bone_store)
					if limb.interaction.autoswitch_keyframe == True:
						ui_layout_non_basic_autoswitch_keyframe_ = ui_layout_non_basic_autoswitch_keyframe.replace("###SWITCH_BONE_STORE###", limb.interaction.bone_store)
						ui_layout_non_basic_autoswitch_ = ui_layout_non_basic_autoswitch_.replace("###GENERATED_interaction_AUTOSWITCH_KEYFRAME###",ui_layout_non_basic_autoswitch_keyframe_)
						ui_layout_non_basic_autoswitch_ = ui_layout_non_basic_autoswitch_.replace("###tab###", tabs)
					else:
						ui_layout_non_basic_autoswitch_ = ui_layout_non_basic_autoswitch_.replace("###GENERATED_interaction_AUTOSWITCH_KEYFRAME###","")

					ui_layout_non_basic_autoswitch_ = ui_layout_non_basic_autoswitch_.replace("###tab###", tabs)
					ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autoswitch_UI###",ui_layout_non_basic_autoswitch_)


				#autodisplay : UI
				if limb.interaction.autodisplay == False:
					ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autodisplay_UI###","")
				else:
					ui_layout_non_basic_autodisplay_ = ui_layout_non_basic_autodisplay.replace("###AUTODISPLAY_BONE_STORE###",limb.interaction.bone_store)
					ui_layout_non_basic_autodisplay_ = ui_layout_non_basic_autodisplay_.replace("###tab###", tabs)
					ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autodisplay_UI###",ui_layout_non_basic_autodisplay_)

				#autokeyframe : UI
				if limb.interaction.autokeyframe == False:
					ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autokeyframe_UI###","")
				else:
					ui_layout_non_basic_autokeyframe_ = ui_layout_non_basic_autokeyframe.replace("###AUTOKEYFRAME_BONE_STORE###",limb.interaction.bone_store)
					ui_layout_non_basic_autokeyframe_ = ui_layout_non_basic_autokeyframe_.replace("###tab###", tabs)
					ui_layout_non_basic_ = ui_layout_non_basic_.replace("###GENERATED_autokeyframe_UI###",ui_layout_non_basic_autokeyframe_)

				ui_layout_non_basic_ = ui_layout_non_basic_.replace("###tab###", tabs)
				total_layout_ = total_layout_ + ui_layout_non_basic_

		ui_generated_text_ = ui_generated_text_.replace("###LAYOUT###", total_layout_)

		if context.active_object.data["autosnap_rig_id"] + "_autosnap_ui.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[context.active_object.data["autosnap_rig_id"] + "_autosnap_ui.py"])
		text = bpy.data.texts.new(name=context.active_object.data["autosnap_rig_id"] + "_autosnap_ui.py")
		text.use_module = True
		text.write(ui_generated_text_)
		exec(text.as_string(), {})

		return {'FINISHED'}


def register():
	bpy.utils.register_class(POSE_OT_juas_limb_switch_ikfk)
	bpy.utils.register_class(POSE_OT_juas_limb_copy)
	bpy.utils.register_class(POSE_OT_juas_generate_snapping)

def unregister():
	bpy.utils.unregister_class(POSE_OT_juas_limb_switch_ikfk)
	bpy.utils.unregister_class(POSE_OT_juas_limb_copy)
	bpy.utils.unregister_class(POSE_OT_juas_generate_snapping)
