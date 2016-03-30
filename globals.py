import bpy

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
switch_type_items = [
	("FORCED", "Forced", "", 1),
	("DEDUCTED", "DEDUCTED", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
switch_invert_items = [
	("IKIS0", "IK is 0", "", 1),
	("FKIS0", "FK is 0", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
switch_forced_value = [
	("IK2FK", "ik2fk", "", 1),
	("FK2IK", "fk2ik", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
autodisplay_items = [
	("LAYER", "Layer", "", 1),
#	("HIDE", "Hide", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
autokeyframe_items = [
	("AVAILABLE", "Available", "", 1),
	("KEYING_SET", "Keying Set", "", 2),
]

### Warning : report new attribute to copy mirror ops
class AutoSnap_DisplayPanel(bpy.types.PropertyGroup):
	bone   = bpy.props.BoolProperty(name="Display Bones Settings", default=False)
	layout = bpy.props.BoolProperty(name="Display Layout Settings", default=False)
	interaction = bpy.props.BoolProperty(name="Display Interaction Settings", default=False)
	
def fct_upd_autoswitch_data_bone(self, context):
	armature = bpy.context.active_object
	armature.limbs[armature.active_limb].layout.switch_bone = armature.limbs[armature.active_limb].interaction.autoswitch_data.bone
	
def fct_upd_autoswitch_data_property(self, context):
	armature = bpy.context.active_object
	armature.limbs[armature.active_limb].layout.switch_property = armature.limbs[armature.active_limb].interaction.autoswitch_data.property
	
def fct_upd_switch_bone(self, context):
	armature = bpy.context.active_object
	armature.limbs[armature.active_limb].interaction.autoswitch_data.bone = armature.limbs[armature.active_limb].layout.switch_bone
	
def fct_upd_switch_property(self, contex):
	armature = bpy.context.active_object
	armature.limbs[armature.active_limb].interaction.autoswitch_data.property = armature.limbs[armature.active_limb].layout.switch_property
	
def fct_upd_basic_layout(self, context):
	armature = bpy.context.active_object
	if armature.limbs[armature.active_limb].layout.basic == True:
		#uncheck interaction
		armature.limbs[armature.active_limb].interaction.autodisplay = False
		armature.limbs[armature.active_limb].interaction.autoswitch = False
		armature.limbs[armature.active_limb].interaction.autoswitch_keyframe = False
		armature.limbs[armature.active_limb].interaction.autokeyframe = False
		armature.limbs[armature.active_limb].display.interaction = False
		
	
### Warning : report new attribute to copy mirror ops
class AutoSnap_Layout_data(bpy.types.PropertyGroup):

	basic = bpy.props.BoolProperty(name="Basic layout", default=True, update=fct_upd_basic_layout)
	
	display_name = bpy.props.BoolProperty(name="Display name", default=True)
	
	fk2ik_label = bpy.props.StringProperty(name="fk2ik label", default="fk2ik")
	ik2fk_label = bpy.props.StringProperty(name="ik2fk label", default="ik2fk")
	
	#SWITCH
	switch_bone = bpy.props.StringProperty(name="Switch Bone", update=fct_upd_switch_bone)
	switch_property = bpy.props.StringProperty(name="Switch Property",update=fct_upd_switch_property)
	switch_invert = bpy.props.EnumProperty(items=switch_invert_items,name="Way", default = "IKIS0")
	
### Warning : report new attribute to copy mirror ops
class AutoSnap_autoswitch_data(bpy.types.PropertyGroup):
	bone = bpy.props.StringProperty(name="Switch Bone", update=fct_upd_autoswitch_data_bone)
	bone_store = bpy.props.StringProperty(name="Switch Bone to store data")
	property = bpy.props.StringProperty(name="Switch Property", update=fct_upd_autoswitch_data_property)
	
### Warning : report new attribute to copy mirror ops
class AutoSnap_autodisplay_data(bpy.types.PropertyGroup):
	bone_store = bpy.props.StringProperty(name="Display Bone to store data")
	type = bpy.props.EnumProperty(name="AutoDisplay type", items=autodisplay_items, default="LAYER")
	layer_ik = bpy.props.BoolVectorProperty(name="Layer IK", subtype='LAYER', size = 32)
	layer_fk = bpy.props.BoolVectorProperty(name="Layer FK", subtype='LAYER', size = 32)
	
### Warning : report new attribute to copy mirror ops
class AutoSnap_autokeyframe_data(bpy.types.PropertyGroup):
	bone_store = bpy.props.StringProperty(name="Display Bone to store data")
	type = bpy.props.EnumProperty(name="AutoKeyframe type", items=autokeyframe_items, default="AVAILABLE")
	keying_set_FK = bpy.props.StringProperty(name="Keying Set FK")
	keying_set_IK = bpy.props.StringProperty(name="Keying Set IK")
	
### Warning : report new attribute to copy mirror ops
class AutoSnap_Interaction(bpy.types.PropertyGroup):
	autoswitch           = bpy.props.BoolProperty(name="Switch FK/IK property", default=False)
	autoswitch_data      = bpy.props.PointerProperty(type=AutoSnap_autoswitch_data)
	autoswitch_keyframe  = bpy.props.BoolProperty(name="Switch FK/IK property, and keyframe it", default=False)
	autodisplay          = bpy.props.BoolProperty(name="Auto display", default=False)
	autodisplay_data     = bpy.props.PointerProperty(type=AutoSnap_autodisplay_data)
	autokeyframe         = bpy.props.BoolProperty(name="Auto Keyframe Chain", default=False)
	autokeyframe_data    = bpy.props.PointerProperty(type=AutoSnap_autokeyframe_data)

class AutoSnap_Generation(bpy.types.PropertyGroup):
	view_location = bpy.props.EnumProperty(name="View location", items=view_location_items, default="TOOLS")
	panel_name    = bpy.props.StringProperty(name="Panel name")
	tab_tool      = bpy.props.StringProperty(name="Tab")

class SideItem(bpy.types.PropertyGroup):
	name_R = bpy.props.StringProperty(name="Side name R")
	name_L = bpy.props.StringProperty(name="Side name L")

### Warning : any modification on this PorpertyGroup must be reported on generated source code
class BoneItem(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone name")
	
### Warning : any modification on this PorpertyGroup must be reported on generated source code
class BonePairItem(bpy.types.PropertyGroup):
	name_FK = bpy.props.StringProperty(name="Bone name FK")
	name_IK = bpy.props.StringProperty(name="Bone name IK")
	
### Warning : report new attribute to copy mirror ops
class LimbItem(bpy.types.PropertyGroup):

	layout  = bpy.props.PointerProperty(type=AutoSnap_Layout_data)
	
	display = bpy.props.PointerProperty(type=AutoSnap_DisplayPanel)
	
	interaction = bpy.props.PointerProperty(type=AutoSnap_Interaction)

	ik_type = bpy.props.EnumProperty(name="IK type", items=IK_type_items, default="POLE")
	ik_scale_type   = bpy.props.EnumProperty(name="IK scale type", items=scale_type_items, default="NONE")
	fk_scale_type   = bpy.props.EnumProperty(name="FK scale type", items=scale_type_items, default="NONE")
	ik_location_type = bpy.props.EnumProperty(name="IK location type", items=location_type_items, default="NONE")
	fk_location_type = bpy.props.EnumProperty(name="FK location type", items=location_type_items, default="NONE")
	global_scale	 = bpy.props.BoolProperty(name="Global scale", default=False)
	with_limb_end_fk	= bpy.props.BoolProperty(name="Limb End FK", default=False)
	with_limb_end_ik	= bpy.props.BoolProperty(name="Limb End IK", default=False)
	with_reinit_bones   = bpy.props.BoolProperty(name="Limb Reinit bones", default=False)
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
	
	fk1  = bpy.props.StringProperty(name="FK 1")
	fk2  = bpy.props.StringProperty(name="FK 2")
	fk3  = bpy.props.StringProperty(name="FK 3")
	fk4  = bpy.props.StringProperty(name="FK toe")
	fk_scale = bpy.props.StringProperty(name="FK Scale")
	fk_location = bpy.props.StringProperty(name="FK location")
	
	reinit_bones = bpy.props.CollectionProperty(type=BoneItem)
	active_reinit_bone = bpy.props.IntProperty()
	
	add_bones = bpy.props.CollectionProperty(type=BonePairItem)
	active_add_bone = bpy.props.IntProperty()

#shortcut to prefs
def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences

def register():
	bpy.utils.register_class(BoneItem)
	bpy.utils.register_class(BonePairItem)
	bpy.utils.register_class(AutoSnap_Layout_data)
	bpy.utils.register_class(AutoSnap_DisplayPanel)
	bpy.utils.register_class(AutoSnap_autoswitch_data)
	bpy.utils.register_class(AutoSnap_autodisplay_data)
	bpy.utils.register_class(AutoSnap_autokeyframe_data)
	bpy.utils.register_class(AutoSnap_Interaction)
	bpy.utils.register_class(LimbItem)
	bpy.utils.register_class(AutoSnap_Generation)

def unregister():
	bpy.utils.unregister_class(LimbItem)
	bpy.utils.unregister_class(AutoSnap_Layout_data)
	bpy.utils.unregister_class(AutoSnap_DisplayPanel)
	bpy.utils.unregister_class(AutoSnap_autoswitch_data)
	bpy.utils.unregister_class(AutoSnap_autodisplay_data)
	bpy.utils.unregister_class(AutoSnap_autokeyframe_data)
	bpy.utils.unregister_class(AutoSnap_Interaction)
	bpy.utils.unregister_class(BoneItem)
	bpy.utils.unregister_class(BonePairItem)
	bpy.utils.unregister_class(AutoSnap_Generation)
