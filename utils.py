import bpy

def get_symm_name(bone):
	#first check if last digit are .xxx with [dot] and then xxx is integer
	end_name = ""
	if bone[len(bone)-4:len(bone)-3] == '.' and bone[len(bone)-3:].isdigit():
		end_pos = len(bone) - 4
		end_name = bone[len(bone)-4:]
	else:
		end_pos = len(bone)
		
		
	#construct dict for each length of potential side
	side_len = {}
	for side in bpy.context.scene.sides: #ADDON when moved to addon pref
		if len(side.name_R) in side_len.keys():
			side_len[len(side.name_R)].append((side.name_R, side.name_L))
		else:
			side_len[len(side.name_R)] = []
			side_len[len(side.name_R)].append((side.name_R, side.name_L))
		if len(side.name_L) in side_len.keys():
			side_len[len(side.name_L)].append((side.name_L, side.name_R))
		else:
			side_len[len(side.name_L)] = []
			side_len[len(side.name_L)].append((side.name_L, side.name_R))
			
	for side_l in side_len.keys():
		if bone[end_pos-side_l:end_pos] in [name[0] for name in side_len[side_l]]:
			return bone[:end_pos-side_l] + side_len[side_l][[name[0] for name in side_len[side_l]].index(bone[end_pos-side_l:end_pos])][1] + end_name
	return bone


def init_sides(context):
	sides = context.scene.sides
	side = sides.add()
	side.name_R = ".R"
	side.name_L = ".L"
	side = sides.add()
	side.name_R = ".r"
	side.name_L = ".l"
	side = sides.add()
	side.name_R = "right"
	side.name_L = "left"
	context.scene.active_side = 2


