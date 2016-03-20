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
		
class POSE_OT_limb_select_bone(bpy.types.Operator):
	"""Set active bone to limb bone"""
	bl_idname = "pose.limb_select_bone"
	bl_label = "Select Limb bone"
	bl_options = {'REGISTER'}
	
	bone = bpy.props.StringProperty()
	
	@classmethod
	def poll(self, context):
		return context.active_object and context.active_object.type == "ARMATURE" and len(context.active_object.limbs) > 0
				
	def execute(self, context):
		armature = context.object
		if context.active_pose_bone:
			bone_name = context.active_pose_bone.name
		
		if self.bone == "root":
			armature.limbs[armature.active_limb].root = bone_name   
		elif self.bone == "ik1":
			armature.limbs[armature.active_limb].ik1 = bone_name
		elif self.bone == "ik2":
			armature.limbs[armature.active_limb].ik2 = bone_name
		elif self.bone == "ik3":
			armature.limbs[armature.active_limb].ik3 = bone_name
		elif self.bone == "ik4":
			armature.limbs[armature.active_limb].ik4 = bone_name
		elif self.bone == "ik5":
			armature.limbs[armature.active_limb].ik5 = bone_name
		elif self.bone == "fk1":
			armature.limbs[armature.active_limb].fk1 = bone_name
		elif self.bone == "fk2":
			armature.limbs[armature.active_limb].fk2 = bone_name
		elif self.bone == "fk3":
			armature.limbs[armature.active_limb].fk3 = bone_name
		elif self.bone == "fk4":
			armature.limbs[armature.active_limb].fk4 = bone_name
		elif self.bone == "ik_scale":
			armature.limbs[armature.active_limb].ik_scale = bone_name
		elif self.bone == "ik_location":
			armature.limbs[armature.active_limb].ik_location = bone_name		
		elif self.bone == "fk_scale":
			armature.limbs[armature.active_limb].fk_scale = bone_name
		elif self.bone == "fk_location":
			armature.limbs[armature.active_limb].fk_location = bone_name	
		elif self.bone == "reinit_bone":
			armature.limbs[armature.active_limb].reinit_bones[armature.limbs[armature.active_limb].active_reinit_bone].name = bone_name
		
	
		return {'FINISHED'}   

def register():
	bpy.utils.register_class(POSE_OT_limb_move)
	bpy.utils.register_class(POSE_OT_limb_add)
	bpy.utils.register_class(POSE_OT_limb_remove)
	
	bpy.utils.register_class(POSE_OT_side_move)
	bpy.utils.register_class(POSE_OT_side_add)
	bpy.utils.register_class(POSE_OT_side_remove)
	
	bpy.utils.register_class(POSE_OT_reinit_bone_move)
	bpy.utils.register_class(POSE_OT_reinit_bone_add)
	bpy.utils.register_class(POSE_OT_reinit_bone_remove)
	
	bpy.utils.register_class(POSE_OT_limb_select_bone)

def unregister():
	bpy.utils.unregister_class(POSE_OT_limb_move)
	bpy.utils.unregister_class(POSE_OT_limb_add)
	bpy.utils.unregister_class(POSE_OT_limb_remove)
	
	bpy.utils.unregister_class(POSE_OT_side_move)
	bpy.utils.unregister_class(POSE_OT_side_add)
	bpy.utils.unregister_class(POSE_OT_side_remove)
	
	bpy.utils.unregister_class(POSE_OT_reinit_bone_move)
	bpy.utils.unregister_class(POSE_OT_reinit_bone_add)
	bpy.utils.unregister_class(POSE_OT_reinit_bone_remove)
	
	bpy.utils.unregister_class(POSE_OT_limb_select_bone)

