import bpy
import mathutils
import math
import uuid
import inspect	

from .globals import *
from .utils import *
from .ui_texts import *

def get_poll_snapping_op(context):
	return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and context.mode == 'POSE'


class POSE_OT_limb_mirror_copy(bpy.types.Operator):
	"""Copy active limb, and mirror it"""
	bl_idname = "pose.limb_mirror_copy"
	bl_label = "Mirror Copy Limb"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
				
	def execute(self, context):

		if len(addonpref().sides) == 0:
			init_sides(context)	

		armature = context.object
		src_limb_index = armature.active_limb
		dst_limb = armature.limbs.add()
		
		dst_limb.name = get_symm_name(armature.limbs[src_limb_index].name)
		
		dst_limb.display.bone   = armature.limbs[src_limb_index].display.bone
		dst_limb.display.layout = armature.limbs[src_limb_index].display.layout
		dst_limb.display.interaction = armature.limbs[src_limb_index].display.interaction
		
		dst_limb.interaction.autoswitch = armature.limbs[src_limb_index].interaction.autoswitch
		dst_limb.interaction.autoswitch_data.bone = armature.limbs[src_limb_index].interaction.autoswitch_data.bone
		dst_limb.interaction.autoswitch_data.property = armature.limbs[src_limb_index].interaction.autoswitch_data.property
		
			
		dst_limb.fk2ik_label = armature.limbs[src_limb_index].fk2ik_label
		dst_limb.ik2fk_label = armature.limbs[src_limb_index].ik2fk_label
		
		dst_limb.switch_bone = get_symm_name(armature.limbs[src_limb_index].switch_bone)
		dst_limb.switch_property = armature.limbs[src_limb_index].switch_property
		dst_limb.switch_invert = armature.limbs[src_limb_index].switch_invert
		
		dst_limb.ik_type = armature.limbs[src_limb_index].ik_type
		dst_limb.ik_scale_type = armature.limbs[src_limb_index].ik_scale_type
		dst_limb.fk_scale_type = armature.limbs[src_limb_index].fk_scale_type
		dst_limb.ik_location_type = armature.limbs[src_limb_index].ik_location_type
		dst_limb.fk_location_type = armature.limbs[src_limb_index].fk_location_type
		dst_limb.global_scale = armature.limbs[src_limb_index].global_scale
		dst_limb.with_limb_end_fk = armature.limbs[src_limb_index].with_limb_end_fk
		dst_limb.with_limb_end_ik = armature.limbs[src_limb_index].with_limb_end_ik
		dst_limb.with_reinit_bones = armature.limbs[src_limb_index].with_reinit_bones
		
		dst_limb.root = get_symm_name(armature.limbs[src_limb_index].root)
		
		dst_limb.ik1 = get_symm_name(armature.limbs[src_limb_index].ik1)
		dst_limb.ik2 = get_symm_name(armature.limbs[src_limb_index].ik2)
		dst_limb.ik3 = get_symm_name(armature.limbs[src_limb_index].ik3)
		dst_limb.ik4 = get_symm_name(armature.limbs[src_limb_index].ik4)
		dst_limb.ik5 = get_symm_name(armature.limbs[src_limb_index].ik5)
		dst_limb.ik_scale = get_symm_name(armature.limbs[src_limb_index].ik_scale)
		dst_limb.ik_location = get_symm_name(armature.limbs[src_limb_index].ik_location)
		
		dst_limb.fk1 = get_symm_name(armature.limbs[src_limb_index].fk1)
		dst_limb.fk2 = get_symm_name(armature.limbs[src_limb_index].fk2)
		dst_limb.fk3 = get_symm_name(armature.limbs[src_limb_index].fk3)
		dst_limb.fk4 = get_symm_name(armature.limbs[src_limb_index].fk4)
		dst_limb.fk_scale = get_symm_name(armature.limbs[src_limb_index].fk_scale)
		dst_limb.fk_location = get_symm_name(armature.limbs[src_limb_index].fk_location)


		for src_bone in armature.limbs[src_limb_index].reinit_bones:
			dst_bone = dst_limb.reinit_bones.add()
			dst_bone.name = get_symm_name(src_bone.name)
		dst_limb.active_reinit_bone = armature.limbs[src_limb_index].active_reinit_bone
		
		armature.active_limb = len(armature.limbs) - 1
			
		return {'FINISHED'}   
		
class POSE_OT_limb_switch_ikfk(bpy.types.Operator):
	"""Switch between IK / FK"""
	bl_idname = "pose.limb_switch_ikfk"
	bl_label = "Switch IK/FK"
	bl_options = {'REGISTER'}	
	
	layout_type = bpy.props.StringProperty()
	
	switch_type  = bpy.props.EnumProperty(items=switch_type_items)
	switch_forced_value = bpy.props.EnumProperty(items=switch_forced_value)
	
	switch_bone = bpy.props.StringProperty()
	switch_property = bpy.props.StringProperty()
	switch_invert   = bpy.props.BoolProperty()
	
	autoswitch = bpy.props.BoolProperty()
	autoswitch_data_bone = bpy.props.StringProperty()
	autoswitch_data_property = bpy.props.StringProperty()
	autoswitch_keyframe = bpy.props.BoolProperty()
	
	global_scale = bpy.props.BoolProperty()
	ik_scale_type = bpy.props.EnumProperty(items=scale_type_items)
	fk_scale_type = bpy.props.EnumProperty(items=scale_type_items)
	ik_location_type = bpy.props.EnumProperty(items=location_type_items)
	fk_location_type = bpy.props.EnumProperty(items=location_type_items)
	with_limb_end_fk	= bpy.props.BoolProperty()
	with_limb_end_ik	= bpy.props.BoolProperty()
	with_reinit_bones   = bpy.props.BoolProperty()
	ik_type = bpy.props.EnumProperty(items=IK_type_items)
	
	
	root = bpy.props.StringProperty()
	ik1 = bpy.props.StringProperty()
	ik2 = bpy.props.StringProperty()
	ik3 = bpy.props.StringProperty()
	ik4 = bpy.props.StringProperty()
	ik5 = bpy.props.StringProperty()
	ik_scale = bpy.props.StringProperty()
	ik_location = bpy.props.StringProperty()
	fk1 = bpy.props.StringProperty()
	fk2 = bpy.props.StringProperty()
	fk3 = bpy.props.StringProperty()
	fk4 = bpy.props.StringProperty()
	fk_scale = bpy.props.StringProperty()
	fk_location = bpy.props.StringProperty()
	reinit_bones = bpy.props.CollectionProperty(type=BoneItem)
	
	@classmethod
	def poll(self, context):
		return get_poll_snapping_op(context)
		
	def layout_check_default(self, context):
		return True, True
		
	def layout_check_default_switch(self, context):
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
		
	def layout_check(self, context, layout_type):
		if layout_type == "DEFAULT":
			return self.layout_check_default(context)
		elif layout_type == "DEFAULT_SWITCH":
			return self.layout_check_default_switch(context)
		
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

		return True, True
		
		
	def fk2ik_check(self, context):
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
			
		if self.with_reinit_bones == False:
			while len(self.reinit_bones) != 0:
				self.reinit_bones.remove(0)
				
		if self.ik4 != "" and self.ik4 not in context.active_object.data.bones.keys():
			self.report({'ERROR'}, "Bone " + self.ik4 + " doesn't exist")
			return False, {'CANCELLED'}
			
		for bone in self.reinit_bones:
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
				self.report({'ERROR'}, "Wrong Bone property")
				return False, {'CANCELLED'}			

		return True, True
		
	def execute(self, context):
	
		status, error = self.layout_check(context, self.layout_type)
		if status == False:
			return error
			
		#No interaction for DEFAULT layout
		if self.layout_type != "DEFAULT":
			status, error = self.interaction_check(context)
			if status == False:
				return error
	
		way = ""
		if self.switch_type == "FORCED" and self.switch_forced_value == "FK2IK":
			way = "FK2IK"
		elif self.switch_type == "FORCED" and self.switch_forced_value == "IK2FK":
			way = "IK2FK"
		elif self.switch_type == "DEDUCTED" and int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property)) == 1.0 and self.switch_invert == False:
			way = "IK2FK"
		elif self.switch_type == "DEDUCTED" and int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property)) == 1.0 and self.switch_invert == True:
			way = "FK2IK"
		elif self.switch_type == "DEDUCTED" and int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property)) == 0.0 and self.switch_invert == False:
			way = "FK2IK"
		elif self.switch_type == "DEDUCTED" and int(context.active_object.pose.bones[self.switch_bone].get(self.switch_property)) == 0.0 and self.switch_invert == True:
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
			self.ik2fk(context.active_object, self.root, self.ik1, self.ik2, self.ik3, self.ik4, self.ik5, self.fk1, self.fk2, self.fk3, self.fk4, self.ik_scale, self.fk_scale, self.ik_location, self.fk_location, self.reinit_bones)
		elif way == "FK2IK":
			self.fk2ik(context.active_object, self.root, self.ik1, self.ik2, self.ik3, self.ik5, self.ik_scale, self.ik_location,  self.fk1, self.fk2, self.fk3, self.fk4, self.fk_scale, self.fk_location)
		
		#AutoSwitch
		if self.layout_type != "DEFAULT": #No interaction for DEFAULT layout
			if self.switch_type == "DEDUCTED" and self.autoswitch == True:
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
								
		return {'FINISHED'}
		
		
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
			
	def ik2fk(self, obj, root_, ik1_, ik2_, ik3_, ik4_, ik5_, fk1_, fk2_, fk3_, fk4_, ik_scale_, fk_scale_, ik_location_, fk_location_, reinit_bones):
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
		
		for bone in reinit_bones:
			obj.pose.bones[bone.name].matrix_basis = mathutils.Matrix()
		
		ik3.matrix = obj.convert_space(ik3, obj.convert_space(fk3, fk3.matrix,'POSE','WORLD'), 'WORLD','POSE')
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
		ik2.scale = obj.convert_space(ik2, obj.convert_space(fk2, fk2.matrix, 'POSE', 'WORLD'), 'WORLD','POSE').to_scale()
		ik2.scale.x = ik2.scale.x / ik1.scale.x / ik_scale_data[0] / root_scale_data[0]
		ik2.scale.y = ik2.scale.y / ik1.scale.y / ik_scale_data[1] / root_scale_data[1]
		ik2.scale.z = ik2.scale.z / ik1.scale.z / ik_scale_data[2] / root_scale_data[2]
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
			
	def fk2ik(self, obj, root_, ik1_, ik2_, ik3_, ik5_, ik_scale_, ik_location_, fk1_, fk2_, fk3_, fk4_, fk_scale_, fk_location_):
		ik1 = obj.pose.bones[ik1_]
		ik2 = obj.pose.bones[ik2_]
		ik3 = obj.pose.bones[ik3_]
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
		
		fk3_current_rotation_mode = fk3.rotation_mode
		ik3_current_rotation_mode = ik3.rotation_mode
		fk3.rotation_mode = 'QUATERNION'
		ik3.rotation_mode = 'QUATERNION'
		fk3.matrix = obj.convert_space(fk3, obj.convert_space(ik3, ik3.matrix,'POSE','WORLD'), 'WORLD','POSE')
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
		
class POSE_OT_generate_snapping(bpy.types.Operator):
	"""Generate snapping"""
	bl_idname = "pose.generate_snapping"
	bl_label = "Generate Snapping"
	bl_options = {'REGISTER'}
	
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0 and context.mode == 'POSE'
		
	def execute(self, context):
		panel_name    = bpy.props.StringProperty(name="Panel name")
		tab_tool      = bpy.props.StringProperty(name="Tab")
		
		if context.active_object.generation.panel_name == "":
			context.active_object.generation.panel_name = "Snapping"
		if context.active_object.generation.tab_tool == "":
			context.active_object.generation.tab_tool = "Snapping"
		
		#Add rig_id custom prop if not exists, and assign a random value
		if context.active_object.data.get('autosnap_rig_id') is None:
			bpy.context.active_object.data['autosnap_rig_id'] = uuid.uuid4().hex
		rig_id = context.active_object.data.get('autosnap_rig_id')
		
		#retrieve FK/IK switch source code
		source, lines = inspect.getsourcelines(getattr(bpy.types, bpy.ops.pose.limb_switch_ikfk.idname()))
		source[0] = source[0].replace(bpy.ops.pose.limb_switch_ikfk.idname(), bpy.ops.pose.limb_switch_ikfk.idname() + "_" + rig_id)
		source[2] = source[2].replace("pose.limb_switch_ikfk", "pose.limb_switch_ikfk_" + rig_id)
		
		generated_text_ops_ = generated_text_ops
		generated_text_ops_ = generated_text_ops_.replace("###rig_id###", rig_id )
		generated_text_ops_ = generated_text_ops_.replace("###CLASS_switch_FKIK###", "".join(source))
		generated_text_ops_ = generated_text_ops_.replace("###CLASS_switch_FKIK_name###", bpy.ops.pose.limb_switch_ikfk.idname() + "_" + rig_id)
			
		if context.active_object.data["autosnap_rig_id"] + "_autosnap_ops.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[context.active_object.data["autosnap_rig_id"] + "_autosnap_ops.py"])
		text = bpy.data.texts.new(name=context.active_object.data["autosnap_rig_id"] + "_autosnap_ops.py")
		text.use_module = True
		text.write(generated_text_ops_)
		exec(text.as_string(), {})
		
		#Generate ui text
		ui_generated_text_ = ui_generated_text
		ui_generated_text_ = ui_generated_text_.replace("###LABEL###", context.active_object.generation.panel_name) 
		ui_generated_text_ = ui_generated_text_.replace("###REGION_TYPE###", context.active_object.generation.view_location) 
		ui_generated_text_ = ui_generated_text_.replace("###CATEGORY###", context.active_object.generation.tab_tool)
		ui_generated_text_ = ui_generated_text_.replace("###rig_id###", rig_id )
		
		if context.active_object.generation.layout_type == "DEFAULT":
			total_layout = ""
			for limb in context.active_object.limbs:
				ui_generated_switch_param_ = ui_generated_switch_param
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###tab###","\t\t")
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
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk1###", limb.fk1)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk2###", limb.fk2)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk3###", limb.fk3)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk4###", limb.fk4)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_scale###", limb.ik_scale)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_scale###", limb.fk_scale)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_location###", limb.ik_location)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_location###", limb.fk_location)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###limb_reinit_bones###", str([bone.name for bone in limb.reinit_bones]))
				
				ui_layout_default_ = ui_layout_default.replace("###limb###", limb.name)
				ui_layout_default_ = ui_layout_default_.replace("###FK2IK_LABEL###", limb.fk2ik_label)
				ui_layout_default_ = ui_layout_default_.replace("###IK2FK_LABEL###", limb.ik2fk_label)
				ui_layout_default_ = ui_layout_default_.replace("###rig_id###", rig_id)
				ui_layout_default_ = ui_layout_default_.replace("###GENERATED_switch_PARAM###",ui_generated_switch_param_)
				
				total_layout = total_layout + ui_layout_default_
				
			ui_generated_text_ = ui_generated_text_.replace("###LAYOUT###", total_layout)

		elif context.active_object.generation.layout_type == "DEFAULT_SWITCH":
			total_layout = ""
			for limb in context.active_object.limbs:
				ui_generated_switch_param_ = ui_generated_switch_param
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###tab###","\t\t")
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
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk1###", limb.fk1)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk2###", limb.fk2)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk3###", limb.fk3)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk4###", limb.fk4)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_scale###", limb.ik_scale)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_scale###", limb.fk_scale)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###ik_location###", limb.ik_location)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###fk_location###", limb.fk_location)
				ui_generated_switch_param_ = ui_generated_switch_param_.replace("###limb_reinit_bones###", str([bone.name for bone in limb.reinit_bones]))
				
				ui_layout_default_switch_ = ui_layout_default_switch.replace("###limb###", limb.name)
				ui_layout_default_switch_ = ui_layout_default_switch_.replace("###FK2IK_LABEL###", limb.fk2ik_label)
				ui_layout_default_switch_ = ui_layout_default_switch_.replace("###IK2FK_LABEL###", limb.ik2fk_label)
				ui_layout_default_switch_ = ui_layout_default_switch_.replace("###rig_id###", rig_id)
				ui_layout_default_switch_ = ui_layout_default_switch_.replace("###GENERATED_switch_PARAM###",ui_generated_switch_param_)

				total_layout = total_layout + ui_layout_default_switch_

			ui_generated_text_ = ui_generated_text_.replace("###LAYOUT###", total_layout)
		
		if context.active_object.data["autosnap_rig_id"] + "_autosnap_ui.py" in bpy.data.texts.keys():
			bpy.data.texts.remove(bpy.data.texts[context.active_object.data["autosnap_rig_id"] + "_autosnap_ui.py"])
		text = bpy.data.texts.new(name=context.active_object.data["autosnap_rig_id"] + "_autosnap_ui.py")
		text.use_module = True
		text.write(ui_generated_text_)
		exec(text.as_string(), {})
		
		return {'FINISHED'}
		

def register():
	bpy.utils.register_class(POSE_OT_limb_switch_ikfk)

	bpy.utils.register_class(POSE_OT_limb_mirror_copy)
	
	bpy.utils.register_class(POSE_OT_generate_snapping)

def unregister():
	bpy.utils.unregister_class(POSE_OT_limb_switch_ikfk)

	bpy.utils.unregister_class(POSE_OT_limb_mirror_copy)
	
	bpy.utils.unregister_class(POSE_OT_generate_snapping)
