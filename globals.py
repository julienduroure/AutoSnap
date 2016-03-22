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

layout_type_items = [
	("DEFAULT", "Default", "", 1),
	("DEFAULT_SWITCH", "Default - switch", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
switch_type_items = [
	("FORCED", "Forced", "", 1),
	("DEDUCTED", "DEDUCTED", "", 2),
]

### Warning : any modification on this enum must be reported on generated source code
switch_forced_value = [
	("IK2FK", "ik2fk", "", 1),
	("FK2IK", "fk2ik", "", 2),
]

### Warning : report new attribute to copy mirror ops
class AutoSnap_DisplayPanel(bpy.types.PropertyGroup):
	bone   = bpy.props.BoolProperty(name="Display Bones Settings", default=False)
	layout = bpy.props.BoolProperty(name="Display Layout Settings", default=False)
	interaction = bpy.props.BoolProperty(name="Display Interaction Settings", default=False)

class AutoSnap_Generation(bpy.types.PropertyGroup):
	view_location = bpy.props.EnumProperty(name="View location", items=view_location_items, default="TOOLS")
	panel_name    = bpy.props.StringProperty(name="Panel name")
	tab_tool      = bpy.props.StringProperty(name="Tab")
	layout_type   = bpy.props.EnumProperty(name="Layout type", items=layout_type_items, default="DEFAULT")

class SideItem(bpy.types.PropertyGroup):
	name_R = bpy.props.StringProperty(name="Side name R")
	name_L = bpy.props.StringProperty(name="Side name L")

### Warning : any modification on this PorpertyGroup must be reported on generated source code
class BoneItem(bpy.types.PropertyGroup):
	name = bpy.props.StringProperty(name="Bone name")

### Warning : report new attribute to copy mirror ops
class LimbItem(bpy.types.PropertyGroup):

	#DEFAULT & DEFAULT_SWITCH
	fk2ik_label = bpy.props.StringProperty(name="fk2ik label", default="fk2ik")
	ik2fk_label = bpy.props.StringProperty(name="ik2fk label", default="ik2fk")
	
	#DEFAULT_SWITCH
	switch_bone = bpy.props.StringProperty(name="Switch Bone")
	switch_property = bpy.props.StringProperty(name="Switch Property")
	switch_invert = bpy.props.BoolProperty(name="Invert", default = False)
	
	display = bpy.props.PointerProperty(type=AutoSnap_DisplayPanel)

	ik_type = bpy.props.EnumProperty(name="IK type", items=IK_type_items, default="POLE")
	ik_scale_type   = bpy.props.EnumProperty(name="IK scale type", items=scale_type_items, default="NONE")
	fk_scale_type   = bpy.props.EnumProperty(name="FK scale type", items=scale_type_items, default="NONE")
	ik_location_type = bpy.props.EnumProperty(name="IK location type", items=location_type_items, default="NONE")
	fk_location_type = bpy.props.EnumProperty(name="FK location type", items=location_type_items, default="NONE")
	global_scale	 = bpy.props.BoolProperty(name="Global scale", default=False)
	with_limb_end_fk	= bpy.props.BoolProperty(name="Limb End FK", default=False)
	with_limb_end_ik	= bpy.props.BoolProperty(name="Limb End IK", default=False)
	with_reinit_bones   = bpy.props.BoolProperty(name="Limb Reinit bones", default=False)

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

#shortcut to prefs
def addonpref():
	user_preferences = bpy.context.user_preferences
	return user_preferences.addons[__package__].preferences

def register():
	bpy.utils.register_class(BoneItem)
	bpy.utils.register_class(AutoSnap_DisplayPanel)
	bpy.utils.register_class(LimbItem)
	bpy.utils.register_class(AutoSnap_Generation)

def unregister():
	bpy.utils.unregister_class(LimbItem)
	bpy.utils.unregister_class(AutoSnap_DisplayPanel)
	bpy.utils.unregister_class(BoneItem)
	bpy.utils.unregister_class(AutoSnap_Generation)
