import bpy

from .globals import *

class AutoSnapPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	sides = bpy.props.CollectionProperty(type=SideItem) 
	active_side = bpy.props.IntProperty()   

	def draw(self, context):
		layout = self.layout
		row_global    = layout.row()
		col = row_global.column()

		row = col.row()
		if len(addonpref().sides) > 0:
			row.template_list("POSE_UL_SideList", "", addonpref(), "sides", addonpref(), "active_side")
		
			col_ = row.column()
			row_ = col_.column(align=True)
			row_.operator("pose.side_add", icon="ZOOMIN", text="")
			row_.operator("pose.side_remove", icon="ZOOMOUT", text="")
			
			row_ = col_.column(align=True)
			row_.separator()
			row_.operator("pose.side_move", icon='TRIA_UP', text="").direction = 'UP'
			row_.operator("pose.side_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

			col_ = row.column()
			row_ = col_.row()
		else:
			pass #TODO add an operator to init sides

            

def register():
	bpy.utils.register_class(SideItem)
	bpy.utils.register_class(AutoSnapPreferences)

def unregister():
	bpy.utils.unregister_class(SideItem)
	bpy.utils.unregister_class(AutoSnapPreferences)
