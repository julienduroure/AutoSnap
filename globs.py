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
from .ui import *

### Warning : any modification on this enum must be reported on generated source code
IK_type_items = [
	("POLE", "With Pole", "", 1),
	("ROTATION", "With Rotation", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
scale_type_items = [
	("NONE", "None", "", 1),
	("PARENT", "Parenting", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
location_type_items = [
	("NONE", "None", "", 1),
	("PARENT", "Parenting", "", 2),
]

view_location_items = [
	("TOOLS", "Tools", "", 1),
	("UI", "Properties", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
switch_invert_items = [
	("IKIS0", "IK is 0", "", 1),
	("FKIS0", "FK is 0", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
switch_way = [
	("IK2FK", "ik2fk", "", 1),
	("FK2IK", "fk2ik", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
autodisplay_items = [
	("LAYER", "Layer", "", 1),
	("HIDE", "Hide", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
autokeyframe_items = [
	("AVAILABLE", "Available", "", 1),
	("KEYING_SET", "Keying Set", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
switch_type_items = [
    ("PROPERTY", "Property", "", 1),
    ("BONE_TRANSFORMATION", "Bone Transformation", "", 2),
]

### Warning : report new attribute to copy ops
class JuAS_DisplayPanel(bpy.types.PropertyGroup):
	bone   = bpy.props.BoolProperty(name="Display Bones Settings", default=False)
	layout = bpy.props.BoolProperty(name="Display Layout Settings", default=False)
	interaction = bpy.props.BoolProperty(name="Display Interaction Settings", default=False)

def fct_upd_autoswitch_data_bone(self, context):
	armature = bpy.context.active_object
	armature.juas_limbs[armature.juas_active_limb].layout.switch_bone = armature.juas_limbs[armature.juas_active_limb].interaction.autoswitch_data.bone

def fct_upd_autoswitch_data_property(self, context):
	armature = bpy.context.active_object
	armature.juas_limbs[armature.juas_active_limb].layout.switch_property = armature.juas_limbs[armature.juas_active_limb].interaction.autoswitch_data.property

def fct_upd_switch_bone(self, context):
	armature = bpy.context.active_object
	armature.juas_limbs[armature.juas_active_limb].interaction.autoswitch_data.bone = armature.juas_limbs[armature.juas_active_limb].layout.switch_bone

def fct_upd_switch_property(self, contex):
	armature = bpy.context.active_object
	armature.juas_limbs[armature.juas_active_limb].interaction.autoswitch_data.property = armature.juas_limbs[armature.juas_active_limb].layout.switch_property

def fct_upd_switch_type(self, contex):
	armature = bpy.context.active_object
	armature.juas_limbs[armature.juas_active_limb].interaction.autoswitch_data.switch_type = armature.juas_limbs[armature.juas_active_limb].layout.switch_type

def fct_upd_basic_layout(self, context):
	armature = bpy.context.active_object
	if armature.juas_limbs[armature.juas_active_limb].layout.basic == True:
		#uncheck interaction
		armature.juas_limbs[armature.juas_active_limb].interaction.autodisplay = False
		armature.juas_limbs[armature.juas_active_limb].interaction.autoswitch = False
		armature.juas_limbs[armature.juas_active_limb].interaction.autoswitch_keyframe = False
		armature.juas_limbs[armature.juas_active_limb].interaction.autokeyframe = False
		armature.juas_limbs[armature.juas_active_limb].display.interaction = False

def update_panel(self, context):
	bpy.utils.unregister_class(POSE_PT_JuAS_Limbs)
	bpy.utils.unregister_class(POSE_PT_JuAS_LimbDetail)
	bpy.utils.unregister_class(POSE_PT_JuAS_LimbDetailBones)
	bpy.utils.unregister_class(POSE_PT_JuAS_LimbDetailLayout)
	bpy.utils.unregister_class(POSE_PT_JuAS_LimbDetailInteraction)
	bpy.utils.unregister_class(POSE_PT_JuAS_Limb_livesnap)
	bpy.utils.unregister_class(POSE_PT_JuAS_Snap_Generate)

	POSE_PT_JuAS_Limbs.bl_category = addonpref().category
	POSE_PT_JuAS_LimbDetail.bl_category = addonpref().category
	POSE_PT_JuAS_LimbDetailBones.bl_category = addonpref().category
	POSE_PT_JuAS_LimbDetailLayout.bl_category = addonpref().category
	POSE_PT_JuAS_LimbDetailInteraction.bl_category = addonpref().category
	POSE_PT_JuAS_Limb_livesnap.bl_category = addonpref().category
	POSE_PT_JuAS_Snap_Generate.bl_category = addonpref().category

	bpy.utils.register_class(POSE_PT_JuAS_Limbs)
	bpy.utils.register_class(POSE_PT_JuAS_LimbDetail)
	bpy.utils.register_class(POSE_PT_JuAS_LimbDetailBones)
	bpy.utils.register_class(POSE_PT_JuAS_LimbDetailLayout)
	bpy.utils.register_class(POSE_PT_JuAS_LimbDetailInteraction)
	bpy.utils.register_class(POSE_PT_JuAS_Limb_livesnap)
	bpy.utils.register_class(POSE_PT_JuAS_Snap_Generate)


### Warning : report new attribute to copy ops
class JuAS_Layout_data(bpy.types.PropertyGroup):

	basic = bpy.props.BoolProperty(name="Basic layout", default=True, update=fct_upd_basic_layout)

	display_name = bpy.props.BoolProperty(name="Display name", default=True)

	on_select = bpy.props.BoolProperty(name="On select", default=False)

	fk2ik_label = bpy.props.StringProperty(name="fk2ik label", default="fk2ik")
	ik2fk_label = bpy.props.StringProperty(name="ik2fk label", default="ik2fk")

	#SWITCH TYPE
	switch_type = bpy.props.EnumProperty(items=switch_type_items, name="Switch Type", default = "PROPERTY", update=fct_upd_switch_type)

	#SWITCH
	switch_bone = bpy.props.StringProperty(name="Switch Bone", update=fct_upd_switch_bone)

	#SWITCH PROPERTY
	switch_property = bpy.props.StringProperty(name="Switch Property",update=fct_upd_switch_property)
	switch_invert = bpy.props.EnumProperty(items=switch_invert_items,name="Way", default = "IKIS0")

    #SWITCH_BONE_TRANSFORMATION
    #TODO

### Warning : report new attribute to copy ops
class JuAS_autoswitch_data(bpy.types.PropertyGroup):
	switch_type = bpy.props.EnumProperty(name="Switch Type", items=switch_type_items, default="PROPERTY")
	bone = bpy.props.StringProperty(name="Switch Bone", update=fct_upd_autoswitch_data_bone)
	property = bpy.props.StringProperty(name="Switch Property", update=fct_upd_autoswitch_data_property)

### Warning : report new attribute to copy ops
class JuAS_autodisplay_data(bpy.types.PropertyGroup):
	type = bpy.props.EnumProperty(name="AutoDisplay type", items=autodisplay_items, default="LAYER")
	layer_ik = bpy.props.BoolVectorProperty(name="Layer IK", subtype='LAYER', size = 32)
	layer_fk = bpy.props.BoolVectorProperty(name="Layer FK", subtype='LAYER', size = 32)
	bone = bpy.props.StringProperty(name="Display Bone")
	property = bpy.props.StringProperty(name="Display Property")
	invert = bpy.props.BoolProperty(name="Invert Property", default=False)

### Warning : report new attribute to copy ops
class JuAS_autokeyframe_data(bpy.types.PropertyGroup):
	type = bpy.props.EnumProperty(name="AutoKeyframe type", items=autokeyframe_items, default="AVAILABLE")
	keying_set_FK = bpy.props.StringProperty(name="Keying Set FK")
	keying_set_IK = bpy.props.StringProperty(name="Keying Set IK")

### Warning : report new attribute to copy ops
class JuAS_Interaction(bpy.types.PropertyGroup):
	autoswitch           = bpy.props.BoolProperty(name="Switch FK/IK property", default=False)
	autoswitch_data      = bpy.props.PointerProperty(type=JuAS_autoswitch_data)
	autoswitch_keyframe  = bpy.props.BoolProperty(name="Switch FK/IK property, and keyframe it", default=False)
	autodisplay          = bpy.props.BoolProperty(name="Auto display", default=False)
	autodisplay_data     = bpy.props.PointerProperty(type=JuAS_autodisplay_data)
	autokeyframe         = bpy.props.BoolProperty(name="Auto Keyframe Chain", default=False)
	autokeyframe_data    = bpy.props.PointerProperty(type=JuAS_autokeyframe_data)
	bone_store           = bpy.props.StringProperty(name="Display Bone to store data")

class JuAS_Generation(bpy.types.PropertyGroup):
	view_location = bpy.props.EnumProperty(name="View location", items=view_location_items, default="TOOLS")
	panel_name    = bpy.props.StringProperty(name="Panel name")
	tab_tool      = bpy.props.StringProperty(name="Tab")

class JuAS_SideItem(bpy.types.PropertyGroup):
	name_R = bpy.props.StringProperty(name="Side name R")
	name_L = bpy.props.StringProperty(name="Side name L")

### Warning : any modification on this PorpertyGroup must be reported on generated source code
class JuAS_BoneItem(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone name")

### Warning : any modification on this PorpertyGroup must be reported on generated source code
class JuAS_BonePairItem(bpy.types.PropertyGroup):
	name_FK = bpy.props.StringProperty(name="Bone name FK")
	name_IK = bpy.props.StringProperty(name="Bone name IK")

### Warning : report new attribute to copy mirror ops
class JuAS_LimbItem(bpy.types.PropertyGroup):

	layout  = bpy.props.PointerProperty(type=JuAS_Layout_data)

	display = bpy.props.PointerProperty(type=JuAS_DisplayPanel)

	interaction = bpy.props.PointerProperty(type=JuAS_Interaction)

	ik_type = bpy.props.EnumProperty(name="IK type", items=IK_type_items, default="POLE")
	ik_scale_type   = bpy.props.EnumProperty(name="IK scale type", items=scale_type_items, default="NONE")
	fk_scale_type   = bpy.props.EnumProperty(name="FK scale type", items=scale_type_items, default="NONE")
	ik_location_type = bpy.props.EnumProperty(name="IK location type", items=location_type_items, default="NONE")
	fk_location_type = bpy.props.EnumProperty(name="FK location type", items=location_type_items, default="NONE")
	global_scale	 = bpy.props.BoolProperty(name="Global scale", default=False)
	with_limb_end_fk	= bpy.props.BoolProperty(name="Limb End FK", default=False)
	with_limb_end_ik	= bpy.props.BoolProperty(name="Limb End IK", default=False)
	with_stay_bones   = bpy.props.BoolProperty(name="Limb Staying bones", default=False)
	with_roll_bones   = bpy.props.BoolProperty(name="Limb Roll bones", default=False)
	with_add_bones      = bpy.props.BoolProperty(name="Limb Additional bones", default=False)

	name = bpy.props.StringProperty(name="Limb Name")
	root = bpy.props.StringProperty(name="Root")
	ik1  = bpy.props.StringProperty(name="IK 1")
	ik2  = bpy.props.StringProperty(name="IK 2")
	ik3  = bpy.props.StringProperty(name="IK Target")
	ik4  = bpy.props.StringProperty(name="IK Pole")
	ik5  = bpy.props.StringProperty(name="IK toe")
	ik_scale = bpy.props.StringProperty(name="IK Scale")
	ik_location = bpy.props.StringProperty(name="IK location")
	ik_mech_foot = bpy.props.StringProperty(name="IK mech foot")

	fk1  = bpy.props.StringProperty(name="FK 1")
	fk2  = bpy.props.StringProperty(name="FK 2")
	fk3  = bpy.props.StringProperty(name="FK 3")
	fk4  = bpy.props.StringProperty(name="FK toe")
	fk_scale = bpy.props.StringProperty(name="FK Scale")
	fk_location = bpy.props.StringProperty(name="FK location")

	roll_bones = bpy.props.CollectionProperty(type=JuAS_BoneItem)
	active_roll_bone = bpy.props.IntProperty()

	add_bones = bpy.props.CollectionProperty(type=JuAS_BonePairItem)
	active_add_bone = bpy.props.IntProperty()

	select_bones = bpy.props.CollectionProperty(type=JuAS_BoneItem)
	active_select_bone = bpy.props.IntProperty()

	stay_bones = bpy.props.CollectionProperty(type=JuAS_BoneItem)
	active_stay_bone = bpy.props.IntProperty()

def register():
	bpy.utils.register_class(JuAS_BoneItem)
	bpy.utils.register_class(JuAS_BonePairItem)
	bpy.utils.register_class(JuAS_Layout_data)
	bpy.utils.register_class(JuAS_DisplayPanel)
	bpy.utils.register_class(JuAS_autoswitch_data)
	bpy.utils.register_class(JuAS_autodisplay_data)
	bpy.utils.register_class(JuAS_autokeyframe_data)
	bpy.utils.register_class(JuAS_Interaction)
	bpy.utils.register_class(JuAS_LimbItem)
	bpy.utils.register_class(JuAS_Generation)

def unregister():
	bpy.utils.unregister_class(JuAS_LimbItem)
	bpy.utils.unregister_class(JuAS_Layout_data)
	bpy.utils.unregister_class(JuAS_DisplayPanel)
	bpy.utils.unregister_class(JuAS_autoswitch_data)
	bpy.utils.unregister_class(JuAS_autodisplay_data)
	bpy.utils.unregister_class(JuAS_autokeyframe_data)
	bpy.utils.unregister_class(JuAS_Interaction)
	bpy.utils.unregister_class(JuAS_BoneItem)
	bpy.utils.unregister_class(JuAS_BonePairItem)
	bpy.utils.unregister_class(JuAS_Generation)
